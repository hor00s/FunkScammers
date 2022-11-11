import json
from pathlib import Path
from typing import Any


__all__ = [
    'Settings'
]


class Settings:
    def __init__(self, settings_path: Path) -> None:
        """A `Settings` instance loads and handles a
        json file

        :param settings_path: A path to a json file
        :type settings_path: Path
        """
        self.settings_path = settings_path

    def __str__(self) -> str:
        return str(self.all)

    def __repr__(self) -> str:
        return f"<Settings({self.all})>"

    @property
    def all(self) -> dict[Any, Any]:
        """Load all the settings contained in the
        provided file

        :return: A dictionary representation of the settings
        :rtype: dict
        """
        with open(self.settings_path, mode='r') as f:
            return dict(json.load(f))

    def get(self, key: Any) -> Any:
        """Get a certain *setting* from the file

        :param key: The name of the *setting*
        :type key: Any
        :return: The value of the provided key
        :rtype: Any
        :raises KeyError: If the asked key does not exist in\
            the provided file
        """
        return self.all[key]

    def set(self, key: Any, value: Any) -> None:
        """Set a certain *setting* to the provided file

        :param key: The name of the *setting*
        :type key: Any
        :param value: The new value which the (new) key\
            will be set to
        :type value: Any
        """
        settings = self.all
        settings[key] = value
        with open(self.settings_path, mode='w') as f:
            json.dump(settings, f, indent=4)
