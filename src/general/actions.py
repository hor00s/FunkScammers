import os
from pathlib import Path
from typing import Generator


def read_file(path: Path) -> str:
    with open(path, mode='r') as f:
        return f.read()

def ascii_filter(sentence: str, min_range: int, max_range: int) -> str:
    return ''.join(
        i if min_range <= ord(i) <= max_range
        else '' for i in sentence
    )

def load_samples(directory: Path) -> Generator[str, None, None]:
    return (
        ascii_filter(
            read_file((Path(f"{directory}/{file}"))), min_range=0, max_range=127
        )
        for file in os.listdir(directory)
    )
