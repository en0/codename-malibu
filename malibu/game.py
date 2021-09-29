import pygame

from malibu_lib.abc import GameABC
from malibu_lib.model import GameSettings, VideoSettings


class MalibuGame(GameABC):

    def startup(self) -> None:
        self.settings_manager.set_defaults(GameSettings(
            video_settings=VideoSettings(),
            input_settings={}
        ))

    def shutdown(self) -> None:
        ...

    def update(self, frame_delta: int) -> None:
        if self.game_input.is_triggered(key=pygame.K_F11):
            self._toggle_full_screen()

    def _toggle_full_screen(self):
        settings = self.settings_manager.get_settings()
        full_screen = settings.video_settings.full_screen
        settings.video_settings.full_screen = not full_screen
        self.settings_manager.set_settings(settings)
