import asyncio
import json
import random
import re
import discord
import datetime
import schedule
import logging
import aiohttp

from functools import partial
from utils import register_command

TECHNOPOLIS_URL = 'https://technopolis1.herokuapp.com/parse/classes/Melding'

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']


@register_command('lunch')
async def lunch(message, client):
    await client.delete_message(message)
    weekend_messages = [
        'Sorry, er på fotballkamp. Det er jo helg!',
        'Kantina er stengt. Det er jo helg! Dra hjem a.'
    ]
    datetime_today = datetime.datetime.today()
    if datetime_today.hour > 14:
        await client.send_message(message.channel, 'Kantina er stengt for idag. Her er morgendagens meny:')
        day_modifier = 0
    else:
        await client.send_message(message.channel, "Halla! Her er dagens fôr:")
        day_modifier = 1
    if datetime_today.isoweekday()-day_modifier > len(days):
        await client.send_message(message.channel, random.choice(weekend_messages))
    else:
        await get_todays_lunch(message.channel, client, day_modifier)


async def get_todays_lunch(channel, client, day_modifier=1):
    async with aiohttp.ClientSession() as session:
        async with session.post(url=TECHNOPOLIS_URL,
                                headers={'X-Parse-Application-Id': 'ff4d19553b1a41ff89df412b6fe51a8e',
                                         'Content-Type': 'application/json',
                                         'X-Parse-Client-Key': 'anything'},
                                data=json.dumps({
                                    'limit': '10',
                                    'where': {
                                        'kategori_navn': {
                                            '$eq': "ISS Restaurant"
                                        },
                                        'publisert': True
                                    },
                                    'order': "-publishedAt",
                                    '_method': "GET"
                                    })
                                ) as r:
            json_body = await r.json()
            today = days[datetime.datetime.today().isoweekday() - day_modifier]
            embed = discord.Embed()
            embed.set_author(name="Lil' Pål's ", icon_url="http://home.ifi.uio.no/paalh/instance/ph.gif")
            embed.colour = discord.Colour.dark_green()
            embed.title = 'Lunch Menu for {}'.format(today)
            embed.set_thumbnail(
                url='https://public-library.safetyculture.io/media/template_117fba83f5414ec78f3e253e355d91ec/8b1457d4-3d6f-4ce9-916d-5356c251cc7d')
            title, text = get_asia_today(json_body['results'])
            embed.add_field(name=title, value=text, inline=False)
            title, text = get_transit(json_body['results'], today)
            embed.add_field(name=title, value=text, inline=False)
            title, text = get_expedition(json_body['results'], today)
            embed.add_field(name=title, value=text, inline=False)
            await client.send_message(channel, embed=embed)


def get_asia_today(result_list):
    for entry in result_list:
        if entry['tekst'] == 'Asia today' or re.match(r'(?:\n|\t|^|\r\n)(.*)(?:\n|\r\n|$)',
                                                      entry['langBeskrivelse']).lastindex == 2:
            return 'Asia today (10:30 - 13:30)', entry['langBeskrivelse'].replace('\t', '')
    return 'Asia today (10:30 - 13:30)', "Ser ikke ut til at det er en asiatisk meny idag :ramen:"


def get_transit(result_list, today):
    tomorrow = '$' if today == 'Friday' else days[days.index(today)+1]
    for entry in result_list:
        menu = re.search(r'Transit.*?{}.*?\n*(.*?)(?:Expedition|{})'.format(today, tomorrow),
                         entry['langBeskrivelse'], flags=re.DOTALL)
        if menu:
            return 'Transit (10:30 - 13:30)', "\n".join(map(lambda x: x.strip(),
                                                        menu.group(1).strip(':\t\r\n').split('\r\n')))
    return 'Transit (10:30 - 13:30)', 'Sorry amigo, fant ikke menyen idag... :shrug:'


def get_expedition(result_list, today):
    tomorrow = '$' if today == 'Friday' else days[days.index(today) + 1]
    for entry in result_list:
        menu = re.search(r'Expedition.*?{}.*?\n*(.*?)(?:Transit|{})'.format(today, tomorrow),
                         entry['langBeskrivelse'], flags=re.DOTALL)
        if menu:
            return 'Expedition (10:30 - 13:30)', "\n".join(map(lambda x: x.strip(),
                                                           menu.group(1).strip(':\t\r\n').split('\r\n')))
    return 'Expedition (10:30 - 13:30)', 'Sorry kompis, fant ikke menyen idag... :shrug:'


logger = logging.getLogger('schedule')


class AsyncSchedule(schedule.Scheduler):
    async def run_pending(self):
        """
        Run all jobs that are scheduled to run.

        Please note that it is *intended behavior that run_pending()
        does not run missed jobs*. For example, if you've registered a job
        that should run every minute and you only call run_pending()
        in one hour increments then your job won't be run 60 times in
        between but only once.
        """
        runnable_jobs = (job for job in self.jobs if job.should_run)
        for job in sorted(runnable_jobs):
            await self._run_job(job)

    async def _run_job(self, job):
        ret = await job.run()
        if isinstance(ret, schedule.CancelJob) or ret is schedule.CancelJob:
            self.cancel_job(job)

    def every(self, interval=1):
        """
        Schedule a new periodic job.

        :param interval: A quantity of a certain time unit
        :return: An unconfigured :class:`Job <Job>`
        """
        job = AsyncJob(interval, self)
        return job


class AsyncJob(schedule.Job):
    async def run(self):
        """
        Run the job and immediately reschedule it.

        :return: The return value returned by the `job_func`
        """
        logger.info('Running job %s', self)
        ret = await self.job_func()
        self.last_run = datetime.datetime.now()
        self._schedule_next_run()
        return ret


async def run_lunch_scheduler(client):

    lunch_channel = discord.Object('502068484684120065')
    # Test channel: lunch_channel = discord.Object('499575848853045270')

    lunch_schedule = AsyncSchedule()

    lunch_time = "10:30"
    lunch_schedule.every().monday.at(lunch_time).do(partial(get_todays_lunch, channel=lunch_channel, client=client))
    lunch_schedule.every().tuesday.at(lunch_time).do(partial(get_todays_lunch, channel=lunch_channel, client=client))
    lunch_schedule.every().wednesday.at(lunch_time).do(partial(get_todays_lunch, channel=lunch_channel, client=client))
    lunch_schedule.every().thursday.at(lunch_time).do(partial(get_todays_lunch, channel=lunch_channel, client=client))
    lunch_schedule.every().friday.at(lunch_time).do(partial(get_todays_lunch, channel=lunch_channel, client=client))

    while True:
        await lunch_schedule.run_pending()
        await asyncio.sleep(60)
