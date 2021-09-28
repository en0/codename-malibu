import pygame
from typing import Optional

from malibu_lib.abc import GameABC
from malibu_lib.model import GameSettings
from malibu_lib.events import *
from malibu_lib.typing import (
    IEventBus,
    IGame,
    IGameInput,
    IGameScene,
    ISettingManager,
)


class MalibuGame(GameABC):

    x = 0

    def startup(self) -> None:
        print("STARTUP")

    def shutdown(self) -> None:
        print("SHUTDOWN")

    def update(self, frame_delta: int) -> None:
        self.x += 1
        if self.x % 100 == 0:
            print(self.x)

        if self.x == 100:
            print("Going full screen")
            settings = self.settings_manager.get_settings()
            settings.video_settings.full_screen = True
            self.settings_manager.set_settings(settings)

        if self.x == 300:
            print("Going NOT full screen")
            settings = self.settings_manager.get_settings()
            settings.video_settings.full_screen = False
            self.settings_manager.set_settings(settings)

        if self.x == 500:
            self.close()
