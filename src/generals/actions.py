import os
from pathlib import Path
from typing import Generator


__all__ = [
    'read_file',
    'ascii_filter',
    'load_samples',
]


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


def load_samples(directory: Path) -> Generator[str, None, None]:
    """Load all .txt (or similar) samples from a directory
    with plain `.read()`

    :param directory: The directory where the samples are located
    :type directory: Path
    :yield: Each iteration yields the whole conent of one file
    :rtype: Generator[str, None, None]
    """    
    return (
        ascii_filter(
            read_file(
                (Path(f"{directory}/{file}"))
            ), min_range=0, max_range=127
        )
        for file in os.listdir(directory)
    )
