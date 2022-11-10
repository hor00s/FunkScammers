import sys
from .cli import cli


def main(*args, **kwargs):
    # If the program runs with command line aruments it will jump to the cli
    if len(args) > 1:
        sys.exit(
            cli(*args, **kwargs)
        )

    return 0
