import json
import re

import discord
import datetime

from utils import register_command
import aiohttp

TECHNOPOLIS_URL = 'https://technopolis1.herokuapp.com/parse/classes/Melding'

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']


@register_command('lunch')
async def get_todays_lunch(message, client):
    await client.delete_message(message)
    await client.send_message(message.channel, "Halla! Her er dagens fôr:")
    async with aiohttp.ClientSession() as session:
        async with session.post(url=TECHNOPOLIS_URL,
                                headers={'X-Parse-Application-Id': 'ff4d19553b1a41ff89df412b6fe51a8e',
                                         'Content-Type': 'application/json',
                                         'X-Parse-Client-Key': 'anything'},
                                data=json.dumps({
                                    'limit': '2',
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
            print(json_body)
            embed = discord.Embed()
            today = days[datetime.datetime.today().isoweekday()-1]
            embed.set_author(name="Lil' Påls ", icon_url="http://home.ifi.uio.no/paalh/instance/ph.gif")
            for entry in json_body['results']:
                embed.colour = discord.Colour.dark_green()
                embed.title = 'Lunch Menu for {}'.format(today)
                embed.set_thumbnail(
                    url='https://public-library.safetyculture.io/media/template_117fba83f5414ec78f3e253e355d91ec/8b1457d4-3d6f-4ce9-916d-5356c251cc7d')
                if entry['tekst'] == 'Asia today':
                    embed.add_field(name=entry['tekst'], value=entry['langBeskrivelse'], inline=False)
                else:
                    # Entry for both 1st floor and 3rd floor restaurant and needs to be split.
                    first_floor = re.search(r'1.etg:.*?{}:(.*?)\n\n'.format(today), entry['langBeskrivelse'], flags=re.DOTALL).group(1)
                    embed.add_field(name='Transit, 1st floor', value=first_floor.strip(), inline=False)
                    second_floor = re.search(r'3.etg:.*?{}:(.*?)(?:\n\n|$)'.format(today), entry['langBeskrivelse'].replace('\t', ''), flags=re.DOTALL).group(1)
                    embed.add_field(name='Expedition, 3rd floor', value=second_floor.strip(), inline=False)
            await client.send_message(message.channel, embed=embed)
