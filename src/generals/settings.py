import os
import json
from pathlib import Path
from typing import Any


__all__ = [
    'Settings'
]


class Settings:
    def __init__(self, settings_path: Path, **conf: Any) -> None:
        """A `Settings` instance loads and handles a
        json file

        :param settings_path: A path to a json file
        :param conf: The initial configuration
        :type settings_path: Path
        """
        self.settings_path = settings_path
        self.conf = conf

    def __str__(self) -> str:
        return str(self.all)

    def __repr__(self) -> str:
        return f"<Settings({self.all})>"

    def __getitem__(self, key: Any):
        return self.all[key]

    def __contains__(self, key: Any) -> bool:
        return key in self.all

    def _checkout(self) -> None:
        """Automatically write if any changes occured in `self.conf`
        """
        if len(self.all) < len(self.conf):
            for i, v in self.conf.items():
                if i not in self.all:
                    self.set(i, v)

        elif len(self.all) > len(self.conf):
            for i, v in self.all.items():
                if i not in self.conf:
                    self.pop(i)

    @property
    def all(self) -> dict[Any, Any]:
        """Load all the settings contained in the
        provided file

        :return: A dictionary representation of the settings
        :rtype: dict
        """
        with open(self.settings_path, mode='r') as f:
            return dict(json.load(f))

    def init(self) -> None:
        if not os.path.exists(self.settings_path):
            with open(self.settings_path, mode='w') as f:
                json.dump(self.conf, f)
        self._checkout()

    def pop(self, key: Any) -> None:
        """Remove a key from the file

        :param key: The name of the key to be removed
        :type key: Any
        """
        settings = self.all
        del settings[key]
        with open(self.settings_path, mode='w') as f:
            json.dump(settings, f)

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

    def items(self):
        return self.all.items()
