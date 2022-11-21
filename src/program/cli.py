import os
from generals import (
    Settings,
    SETTINGS,
    SCAM_SAMPLES,
    ERROR_LOGGER,
    DEF_SETTINGS,
    actions
)

type_commands = (
    "mypy generals/actions.py --strict",
    "mypy generals/constants.py --strict",
    "mypy generals/settings.py --strict",
    "mypy bot/bot.py --strict",
    "mypy models/model.py --strict"
)

unittest_commands = (
    "python3 -m unittest generals/test_actions.py",
    "python3 -m unittest bot/test_bot.py",
    "python3 -m unittest models/test_models.py",
)

settings_manager = Settings(
    SETTINGS,
    **DEF_SETTINGS
)
settings_manager.init()


def cli(*args, **kwargs):
    """The cli of the. This is it runs
    if the program was triggered with command line arguments
    """
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
        elif args[2] == 'init':
            settings_manager.init()

    # ./funcscammers sample "The text that is supposed to be in the file"
    # (preferably in one line)"
    elif args[1] == 'sample':
        if len(args) > 3:
            raise ValueError('`samples` command takes the\
text in double quotes (`"text that you want to write"`)')
        actions.append_sample(SCAM_SAMPLES, args[2])

    # ./funcscammers lasterror
    elif args[1] == 'lasterror':
        a = actions.read_file(ERROR_LOGGER)
        print(a.split('---------------------------')[-2])
        pass
