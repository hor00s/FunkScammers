from __future__ import annotations
import os
import sys
from enum import Enum
from typing import (
    Optional,
    Tuple,
    Dict,
    List,
    Any,
)

__name__ = 'testing'

__all__ = [
    'UnhandledLogError',
    'get_color',
    'Logger',
]


class Color(Enum):
    # Color end string, color reset
    RESET = "\033[0m"
    # Regular Colors. Normal color, no bold, background color etc.
    BLACK = "\033[0;30m"    # BLACK
    RED = "\033[0;31m"      # RED
    GREEN = "\033[0;32m"    # GREEN
    YELLOW = "\033[0;33m"   # YELLOW
    BLUE = "\033[0;34m"     # BLUE
    MAGENTA = "\033[0;35m"  # MAGENTA
    CYAN = "\033[0;36m"     # CYAN
    WHITE = "\033[0;37m"    # WHITE
    # Bold colors
    BLACK_BOLD = "\033[1;30m"    # BLACK
    RED_BOLD = "\033[1;31m"      # RED
    GREEN_BOLD = "\033[1;32m"    # GREEN
    YELLOW_BOLD = "\033[1;33m"   # YELLOW
    BLUE_BOLD = "\033[1;34m"     # BLUE
    MAGENTA_BOLD = "\033[1;35m"  # MAGENTA
    CYAN_BOLD = "\033[1;36m"     # CYAN
    WHITE_BOLD = "\033[1;37m"    # WHITE


def get_color(color: str) -> str:
    return getattr(Color, color.upper()).value  # type: ignore


class Config:
    _INSTANCE = 0

    def __init__(self, level: int) -> None:
        Config._INSTANCE += 1
        self._INSTANCE = Config._INSTANCE
        self._settings = {
            'success': 2,
            'info': 3,
            'custom': 2,
            'warning': 1,
            'error': 1,
            'debug': 2,
        }
        self.level = level
        self._iter = 0

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}({self._settings})>"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(settings={self._settings},\
 level={self._level} instance={self._INSTANCE})>"

    def __bool__(self) -> bool:
        return bool(self._settings)

    def __getitem__(self, k: str) -> int:
        return self._settings[k]

    def __int__(self) -> int:
        return self.level

    def __len__(self) -> int:
        return len(self._settings)

    def __contains__(self, __o: Any) -> bool:
        return __o in self._settings

    def __iter__(self) -> Config:
        return self

    def __next__(self) -> str:
        keys = self.keys()
        if self._iter >= len(self):
            self._iter = 0
            raise StopIteration
        retval = keys[self._iter]
        self._iter += 1
        return retval

    @property
    def settings(self) -> Dict[str, int]:
        return self._settings

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, v: int) -> None:
        """Level setter validator

        :param v: The level to change to
        :type v: int
        :raises ValueError: If the v is invalid for `level`
        """
        if not 0 < v <= 5:
            raise ValueError(f"Level must be between `0-5` not `{v}`")
        self._level = v

    def items(self):  # type: ignore
        yield self._settings.items()

    def keys(self) -> List[str]:
        return list(self._settings.keys())

    def values(self) -> List[int]:
        return list(self._settings.values())

    def update(self, **settings: int) -> None:
        """Change the settings configuration for a given instance

        :raises ValueError: If the configuraion does not exist or\
            user tries to update to an invalid value
        """
        if all(key in self.settings for key in settings) and\
           all(0 < settings[key] <= 5 for key in settings):
            self._settings.update(settings)
        else:
            raise ValueError(f"Invalid key or value in {settings}. Remember,\
 key has to exists in {self.settings} and all values have to be between (1-5)")

    def get(self, key: str) -> int:
        """Get a setting configuration

        :param key: Key of the configuration
        :type key: str
        :return: The level this configuration is set to
        :rtype: int
        """
        return self._settings[key]


class UnhandledLogError(Exception): ...


class MetaLogger(type):
    """A simple metaclass that checks if all logs/settings are correctly
    handled by comaring the ammount of settings in Config._settings agnainst
    the functions that live in Logger() - some unnecessary
    """
    def __new__(self, name: str, bases:
                Tuple[type], attrs: Dict[str, Any]) -> type:
        error_msg = "We either have a log function that is not in settings OR\
 a function that needs to be dissmissed OR a setting that is\
 not added as a log function"

        log_functions = 0
        target_log_functions = len(Config(1))
        dismiss_attrs = ('settings',)
        for log in attrs:
            if not log.startswith('_') and log not in dismiss_attrs:
                log_functions += 1
        if not log_functions == target_log_functions:
            raise UnhandledLogError(error_msg)
        return type(name, bases, attrs)


class Logger(metaclass=MetaLogger):
    """The Logger class handles debbuging with colored information
    based on the level. Each instance has its own settings which the
    user can change independently through `self.settings.update()`.
    Mind that level 1 will print evetything and level 5 less
    """
    def __init__(self, level: int = 2, log_path: Optional[str] = None):
        """Initializer of Logger object

        :param level: The level of debugging. Based on that, some informations\
            can be configured to not show up thus lowering the verbosity, defaults to 2
        :type level: int, optional
        """
        self._settings = Config(level)
        self._log_path = log_path

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}Object-{self._settings._INSTANCE}>"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(instance={self._settings._INSTANCE})>"

    @property
    def settings(self) -> Config:
        """Getter so self._settings cannot be writable

        :return: Config instance
        :rtype: Config
        """
        return self._settings

    def _log(self, header: str, msg: str) -> None:
        if self._log_path is not None:
            if not os.path.exists(self._log_path):
                with open(self._log_path, mode='w') as _: ...
            with open(self._log_path, mode='a') as f:
                f.write(f"[{header.upper()}]: {msg}\n")

    def _runner(self, func_name: str) -> bool:
        """Use to check the `self.level` before printing the log

        :param func_name: Name of the function as a string
        :type func_name: str
        :return: Wheather the settings allow this certain function to print
        :rtype: bool
        """
        return self.settings.level <= self.settings[func_name]

    # ONLY LOGGING FUNCTIONS AFTER THIS
    def custom(self, msg: str, header: str = 'custom',
               *args: Any, color: str = get_color('reset'), **kwargs: Any) -> None:
        func_name = sys._getframe().f_code.co_name
        if self._runner(func_name):
            print(f"{color}[{header.upper()}]: {msg}{get_color('reset')}", *args, **kwargs)
        self._log(header, msg)

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        func_name = sys._getframe().f_code.co_name
        if self._runner(func_name):
            print(f"{Color.YELLOW.value}[{func_name.upper()}]: {msg}{get_color('reset')}",
                  *args, **kwargs)
        self._log(func_name, msg)

    def success(self, msg: str, *args: Any, **kwargs: Any) -> None:
        func_name = sys._getframe().f_code.co_name
        if self._runner(func_name):
            print(f"{Color.GREEN.value}[{func_name.upper()}]: {msg}{get_color('reset')}",
                  *args, **kwargs)
        self._log(func_name, msg)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        func_name = sys._getframe().f_code.co_name
        if self._runner(func_name):
            print(f"{Color.RED.value}[{func_name.upper()}]: {msg}{get_color('reset')}",
                  *args, **kwargs)
        self._log(func_name, msg)

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        func_name = sys._getframe().f_code.co_name
        if self._runner(func_name):
            print(f"{Color.RED_BOLD.value}[{func_name.upper()}]: {msg}{get_color('reset')}",
                  *args, **kwargs)
        self._log(func_name, msg)

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        func_name = sys._getframe().f_code.co_name
        if self._runner(func_name):
            print(f"{Color.BLUE.value}[{func_name.upper()}]: {msg}{get_color('reset')}",
                  *args, **kwargs)
        self._log(func_name, msg)
