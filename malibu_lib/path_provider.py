from os import makedirs
from os.path import join as join_path, exists
from appdirs import user_log_dir, user_config_dir, user_data_dir

from .typing import IPathProvider
from .model import GameConfig


class UserPathProvider(IPathProvider):

    def get_log_path(self, name: str, version: str=None) -> str:
        return join_path(self._get_log_dir(version), name)

    def get_config_path(self, name: str, version: str=None) -> str:
        return join_path(self._get_config_dir(version), name)

    def get_data_path(self, name: str, version: str=None) -> str:
        return join_path(self._get_data_dir(version), name)

    def ensure_log_dir_exists(self, version: str=None) -> None:
        d = self._get_log_dir(version)
        if not exists(d): makedirs(d)

    def ensure_config_dir_exists(self, version: str=None) -> None:
        d = self._get_config_dir(version)
        if not exists(d): makedirs(d)

    def ensure_data_dir_exists(self, version: str=None) -> None:
        d = self._get_data_dir(version)
        if not exists(d): makedirs(d)

    def _get_log_dir(self, ver) -> None:
        return user_log_dir(
            appname=self._game,
            appauthor=self._author,
            version=ver or self._ver)

    def _get_data_dir(self, ver) -> None:
        return user_data_dir(
            appname=self._game,
            appauthor=self._author,
            version=ver or self._ver)

    def _get_config_dir(self, ver) -> None:
        return user_config_dir(
            appname=self._game,
            appauthor=self._author,
            version=ver or self._ver)

    def __init__(self, config: GameConfig):
        self._game = config.name
        self._author = config.author
        self._ver = config.version

