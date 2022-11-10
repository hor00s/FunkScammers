import os


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


def cli(*args, **kwargs):
    if args[1] == 'unit':  # Shift fot unit test
        for i in unittest_commands:
            os.system(i)
    elif args[1] == 'type':  # Short for type checking\
        for i in type_commands:
            os.system(i)
    elif args[1] == 'allchecks':
        checks = type_commands + unittest_commands
        for i in checks:
            os.system(i)
    return 0
