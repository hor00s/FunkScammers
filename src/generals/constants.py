from pathlib import Path
from typing import TypedDict


__all__ = [
    'SETTINGS',
    'SCAM_SAMPLES',
    'ERROR_LOGGER',
    'DEF_SETTINGS',
    'BASE_DIR',
    'WORTH_LOG',
]


class Conf(TypedDict):
    sus_text_above: str
    max_downvotes: str
    total_matches: str
    top_upvotes: str
    max_posts_lookup: str


BASE_DIR:     Path = Path(__file__).parent.parent.parent
SETTINGS:     Path = Path(f'{BASE_DIR}/settings.json')
SCAM_SAMPLES: Path = Path(f'{BASE_DIR}/samples.csv')
ERROR_LOGGER: Path = Path(f'{BASE_DIR}/error_logs.txt')
WORTH_LOG:    Path = Path(f'{BASE_DIR}/.logs.txt')
DEF_SETTINGS: Conf = {
    "sus_text_above": "0.92",
    "max_downvotes": "-3",
    "total_matches": "2",
    "top_upvotes": "10",
    "max_posts_lookup": "50",
    "worth_logging": "0.1",
    "abort_chars": ['/s', '/j'],
    "total_runs": 0,
    "reset_logs_after": 5,
}
