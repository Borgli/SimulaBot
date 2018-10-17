import random

from utils import register_command_no_prefix


@register_command_no_prefix('professor', 'prof', 'professoren')
async def blush(message, client):
    await client.send_message(message.channel, ':relaxed:')


@register_command_no_prefix('hi', 'hei', 'hello', 'halla')
async def greet(message, client):
    greetings = [
        'Halla!',
        'Yo!',
        'Hva skjer a?',
        'Heisann sveisann.',
        'Hola señorita :man_dancing:',
    ]
    await client.send_message(message.channel, random.choice(greetings))


@register_command_no_prefix('cola')
async def cola(message, client):
    await client.send_message(message.channel, '... og bolle? :yum:')


@register_command_no_prefix('bolle', 'bollerun')
async def bolle(message, client):
    await client.send_message(message.channel, '... og cola? :yum:')


@register_command_no_prefix('syk', 'sick')
async def bolle(message, client):
    await client.send_message(message.channel, 'Uffda! God bedring :bouquet:')


@register_command_no_prefix('"professor da"')
async def greet(message, client):
    await client.send_message(message.channel, 'Hihihi :relaxed:')
