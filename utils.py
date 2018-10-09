from functools import wraps

commands = dict()


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


class CommandAlreadyExistsError(BaseException):
    def __init__(self, command):
        super(CommandAlreadyExistsError, self).__init__("Command '{}' already exists!".format(command))