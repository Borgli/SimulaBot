import discord
import utils
import tokenize
import io

from plugins import *

commands = utils.commands
no_prefix_commands = utils.no_prefix_commands


class Bot(discord.Client):
    def __init__(self, **options):
        super().__init__(**options)
        self.prefix = '!'
        utils.bot = self

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print(discord.version_info)
        print(discord.__version__)
        print('------')

    async def on_message(self, message):
        cmd = message.content

        if len(cmd.split()) < 1 or message.author.id == self.user.id:
            return

        # Normal commands can be awaited and is therefore in their own functions
        for key in commands:
            if cmd.lower().split()[0] == self.prefix + key:
                await commands[key](message, self)
                return

        tokenized_cmd = list(tokenize.generate_tokens(io.StringIO(cmd.lower()).readline))
        for key in no_prefix_commands:
            if list(filter(lambda token: token[1] == key.lower(), tokenized_cmd)):
                await no_prefix_commands[key.lower()](message, self)
                return


def run_bot():
    client = Bot()

    # Reads token
    with open("token.txt", 'r') as f:
        token = f.read().strip()

    # Starts the execution of the bot
    client.run(token)


if __name__ == '__main__':
    run_bot()


