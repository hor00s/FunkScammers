import json
from pathlib import Path
from typing import Any


__all__ = [
    'Settings'
]


class Settings:
    def __init__(self, settings_path: Path) -> None:
        self.settings_path = settings_path

    def __str__(self) -> str:
        return str(self.all)

    def __repr__(self) -> str:
        return f"<Settings({self.all})>"

    @property
    def all(self) -> Any:
        with open(self.settings_path, mode='r') as f:
            return json.load(f)

    def get(self, key: Any) -> Any:
        return self.all[key]

    def set(self, key: Any, value: Any) -> None:
        settings = self.all
        settings[key] = value
        with open(self.settings_path, mode='w') as f:
            json.dump(settings, f, indent=4)
