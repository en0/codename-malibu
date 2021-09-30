from os.path import exists
from typing import Optional
from yaml import safe_load, safe_dump

from .model import GameSettings, GameConfig
from .typing import ISettingManager, IPathProvider
from .events import publish_game_event, SETTINGS_CHANGED


class YamlSettingsManager(ISettingManager):

    def get_settings(self) -> GameSettings:
        if not self._settings:
            self._load_from_disk_or_default()
        return self._settings

    def set_settings(self, settings: GameSettings) -> None:
        self._settings = settings
        self._write_to_disk()
        publish_game_event(SETTINGS_CHANGED, settings=settings)

    def _load_from_disk_or_default(self):
        if not exists(self._path):
            self._settings = self._defaults
            self._write_to_disk()
        else:
            with open(self._path, "r") as fd:
                dat = safe_load(fd)
            self._settings = GameSettings.load(dat)

    def _write_to_disk(self):
        self._path_provider.ensure_config_dir_exists()
        with open(self._path, "w") as fd:
            safe_dump(self._settings.todict(), fd)

    def __init__(self, game_config: GameConfig, path_provider: IPathProvider):
        self._path_provider = path_provider
        self._path = path_provider.get_config_path("game-settings.yaml")
        self._settings: Optional[GameSettings] = None
        self._defaults: GameSettings = game_config.default_settings

