import sys
from .cli import cli
from .mainloop import mainloop


def main(*args, **kwargs):
    """
    The main function of the program which will trigger the
    appropriate function depending on whether the application
    was triggered with command line arguments or not
    """
    if len(args) > 1:
        sys.exit(
            cli(*args, **kwargs)
        )
    else:
        mainloop()

    return 0
