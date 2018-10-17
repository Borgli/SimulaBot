import sys
from functools import wraps

commands = dict()
no_prefix_commands = dict()
bot = None


# Registers new commands
def register_command(*args):
    def wrapper(func):
        for command in args:
            if command in commands:
                raise CommandAlreadyExistsError(command)
            commands[command] = func

        @wraps(func)
        async def wrapped(message, bot_channel, client):
            return await func(message, bot_channel, client)

        return wrapped

    return wrapper


# Registers new commands
def register_command_no_prefix(*args):
    def wrapper(func):
        for command in args:
            if command in no_prefix_commands:
                raise CommandAlreadyExistsError(command)
            no_prefix_commands[command] = func

        @wraps(func)
        async def wrapped(message, bot_channel, client):
            return await func(message, bot_channel, client)

        return wrapped

    return wrapper


class CommandAlreadyExistsError(BaseException):
    def __init__(self, command):
        super(CommandAlreadyExistsError, self).__init__("Command '{}' already exists!".format(command))
