import os

import dateutil
import discord

from utils import register_command
from plugins.lunch import AsyncSchedule

CAKE_CHANNEL = discord.Object("486520695908728832")


@register_command('cake')
async def cake(message, client):
    parameters = message.content.split[1:]
    if parameters:
        datetime = dateutil.parser.parse(parameters[0])
        with open(os.path.dirname(__file__), 'w') as f:
            f.write(datetime)
    else:
        await client.send_message(CAKE_CHANNEL,
                                  "Hallelujah! Det er kaketorsdag idag! :confetti_ball: "
                                  "Cake today at 14:00 in Pusterommet! :cake:")


async def run_cake_scheduler(client):
    scheduler = AsyncSchedule
