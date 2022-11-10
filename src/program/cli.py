import os
from generals import (
    Settings,
    SETTINGS,
)

type_commands = (
    "mypy generals/actions.py --strict",
    "mypy generals/constants.py --strict",
    "mypy generals/settings.py --strict",
    "mypy bot/bot.py --strict",
)

unittest_commands = (
    "python3 -m unittest generals/test_actions.py",
    "python3 -m unittest bot/test_bot.py",
)

settings_manager = Settings(SETTINGS)


def cli(*args, **kwargs):
    # ./funcscammers unit (run unittest tests)
    if args[1] == 'unit':
        for i in unittest_commands:
            os.system(i)

    # ./funcscammers type (run type checks)
    elif args[1] == 'type':
        for i in type_commands:
            os.system(i)

    # ./funcscammers allchecks (run unittest and type checks)
    elif args[1] == 'allchecks':
        checks = type_commands + unittest_commands
        for i in checks:
            os.system(i)

    elif args[1] == 'settings':
        # # ./funcscammers settings get key
        if args[2] == 'get':
            print(settings_manager.get(args[3]))
        # ./funcscammers settings set -key value
        elif args[2] == 'set':
            key = args[3][1:]
            value = args[4]
            settings_manager.set(key, value)

    return 0
