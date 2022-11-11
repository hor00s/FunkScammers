import os
from pathlib import Path
from generals import (
    Settings,
    SETTINGS,
    SCAM_SAMPLES,
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

    # ./funcscammers sample "The text that is supposed to be in the file"
    # (preferably in one line)"
    elif args[1] == 'sample':
        if len(args) > 3:
            raise ValueError('`samples` command takes the\
text in double quotes (`"text that you want to write"`)')

        current_samples = os.listdir(SCAM_SAMPLES)
        find_next_num = max(int(i[:i.index('.')]) for i in current_samples) + 1
        next_file = f"{find_next_num}.txt"
        with open(Path(f"{SCAM_SAMPLES}/{next_file}"), mode='w') as f:
            f.write(args[2])

    return 0
