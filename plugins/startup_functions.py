# register functions to be called on bot startup
import asyncio
import discord
import datetime


async def run_scheduler(client):
    import schedule
    import logging
    from functools import partial
    from plugins.lunch import get_todays_lunch
    lunch_channel = discord.Object('502068484684120065')
    # Test channel: lunch_channel = discord.Object('499575848853045270')
    logger = logging.getLogger('schedule')

    class LunchSchedule(schedule.Scheduler):
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
            job = LunchJob(interval, self)
            return job

    class LunchJob(schedule.Job):
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

    lunch_schedule = LunchSchedule()

    lunch_time = "09:00"
    lunch_schedule.every().monday.at(lunch_time).do(partial(get_todays_lunch, channel=lunch_channel, client=client))
    lunch_schedule.every().tuesday.at(lunch_time).do(partial(get_todays_lunch, channel=lunch_channel, client=client))
    lunch_schedule.every().wednesday.at(lunch_time).do(partial(get_todays_lunch, channel=lunch_channel, client=client))
    lunch_schedule.every().thursday.at(lunch_time).do(partial(get_todays_lunch, channel=lunch_channel, client=client))
    lunch_schedule.every().friday.at(lunch_time).do(partial(get_todays_lunch, channel=lunch_channel, client=client))

    while True:
        await lunch_schedule.run_pending()
        await asyncio.sleep(1)
