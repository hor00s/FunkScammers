from pathlib import Path
from typing import TypedDict


__all__ = [
    'SETTINGS',
    'SCAM_SAMPLES',
    'ERROR_LOGGER',
    'DEF_SETTINGS',
]


class Conf(TypedDict):
    sus_text_above: str
    max_downvotes: str
    total_matches: str
    top_upvotes: str
    max_posts_lookup: str


SETTINGS:     Path = Path('../settings.json')
SCAM_SAMPLES: Path = Path('../samples.csv')
ERROR_LOGGER: Path = Path('../error_logs.txt')
DEF_SETTINGS: Conf = {
    "sus_text_above": "0.92",
    "max_downvotes": "-3",
    "total_matches": "2",
    "top_upvotes": "10",
    "max_posts_lookup": "50"
}
