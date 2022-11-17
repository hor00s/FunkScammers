from pathlib import Path


__all__ = [
    'SETTINGS',
    'SCAM_SAMPLES',
    'ERROR_LOGGER',
]


SETTINGS:     Path = Path('../settings.json')
SCAM_SAMPLES: Path = Path('../samples.csv')
ERROR_LOGGER: Path = Path('../error_logs.txt')
