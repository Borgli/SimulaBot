from utils import register_command


@register_command('lunch')
async def get_todays_lunch(message, client):
    await client.send_message(message.channel, 'Lunch.')
