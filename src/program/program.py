from .cli import cli
from generals import actions
from generals.constants import ERROR_LOGGER
from .mainloop import mainloop


@actions.error_logger(ERROR_LOGGER)
def main(*args, **kwargs):
    """
    The main function of the program which will run the
    appropriate function depending on whether the application
    was triggered with command line arguments or not
    """
    if len(args) > 1:
        cli(*args, **kwargs)
    else:
        mainloop()

    return 0
