from utils import register_command_no_prefix


@register_command_no_prefix('professor', 'prof', 'professoren')
async def blush(message, client):
    await client.send_message(message.channel, ':relaxed:')


@register_command_no_prefix('hi', 'hei', 'hello', 'halla')
async def greet(message, client):
    await client.send_message(message.channel, 'Hello there.')


@register_command_no_prefix('"professor da"')
async def greet(message, client):
    await client.send_message(message.channel, 'Hihihi :relaxed:')
