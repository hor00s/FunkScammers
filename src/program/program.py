from .cli import cli  # type: ignore
from .mainloop import mainloop  # type: ignore
from typing import Any
from generals import actions
from generals.constants import ERROR_LOGGER


@actions.error_logger(ERROR_LOGGER)
def main(*args: Any, **kwargs: Any) -> int:
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
