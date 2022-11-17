import os
import csv
import sys
import traceback
from pathlib import Path
from typing import (
    Generator,
    Callable,
    Any,
)


__all__ = [
    'error_logger',
    'read_file',
    'total_samples',
    'ascii_filter',
    'load_samples',
    'is_imported',
    'append_sample',
]


def write_error(error: Exception, path: Path) -> None:
    with open(path, mode='a') as f:
        error_format = f"""
---------------------------
Short error: {error}

Detailed: {traceback.format_exc()}
---------------------------

        """
        f.write(error_format)


def create_error_logger(path: Path) -> None:
    if not os.path.exists(path):
        with open(path, mode='w') as _: ...


def error_logger(path: Path) -> Callable[[Any], Any]:
    create_error_logger(path)

    def decorator(func: Callable[[Any], int]) -> Callable[[Any], Any] | int:
        def wrapper(*args: Any, **kwargs: Any) -> Callable[[Any], Any] | int:
            try:
                return func(*args, **kwargs)
            except ModuleNotFoundError as err:
                print(err)
                print(traceback.format_exc())
                return 1
            except Exception as err:
                print(err)
                print(traceback.format_exc())
                write_error(err, path)
                return 1
        return wrapper
    return decorator


def read_file(path: Path) -> str:
    """Reads one file at the provided path at plain\
        'r' (read) mode

    :param path: The path where the file is located
    :type path: Path
    :return: The whole content of the file as **1 string (str)**
    :rtype: str
    """
    with open(path, mode='r') as f:
        return f.read()


def total_samples(path: Path) -> int:
    with open(path, mode='r') as f:
        return len(f.readlines())


def ascii_filter(sent: str, min_range: int = 0, max_range: int = 127) -> str:
    """Removes every character that is **less** that min_range **or**
    more that the **max_range** in an attempt to remove emojis or
    other un-wanted characters

    :param sent: The whole string that needs to be filtered\
        (A whole reply for example)
    :type sent: str
    :param min_range: The minimum ascii value of\
        characters we want to keep, defaults to 0
    :type min_range: int, optional
    :param max_range: The maximum ascii value of\
        characters we want to keep, defaults to 127
    :type max_range: int, optional
    :return: The same string only the charactes\
        that are in between the `min_range` and `max_range`
    :rtype: str
    """
    return ''.join(
        i if min_range <= ord(i) <= max_range
        else '' for i in sent
    )


def load_samples(path: Path) -> Generator[str, None, None]:
    """Load all .txt (or similar) samples from a directory
    with plain `.read()`

    :param directory: The directory where the samples are located
    :type directory: Path
    :yield: Each iteration yields the whole conent of one file
    :rtype: Generator[str, None, None]
    """
    with open(path, mode='r') as f:
        reader = csv.reader(f)
        for row in reader:
            yield ascii_filter(row[0])


def is_imported(module: Any | object) -> bool:
    return module in sys.modules


def append_sample(path: Path, text: str) -> None:
    with open(path, mode='a') as f:
        f.write('\n' + text)
