import sys
from .cli import cli


def main(*args, **kwargs):
    if len(args) > 1:
        sys.exit(
            cli(*args, **kwargs)
        )

    print('mainloop')
    return 0
