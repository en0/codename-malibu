import pygame
from typing import Optional

from malibu_lib.model import GameSettings
from malibu_lib.typing import (
    IGame,
    IGameScene,
    IGameInput,
    ISettingManager,
)


class MalibuGame(IGame):
    def set_scene(self, next_scene: IGameScene) -> None:
        if self.scene:
            self.scene.shutdown()
        self.scene = next_scene
        self.scene.startup()

    def play(self) -> None:
        self.is_playing = True
        while self.is_playing:
            delta = self.clock.tick(self.frame_rate)
            self.do_events()
            self.do_update(delta)
            self.do_render()

    def close(self) -> None:
        self.is_playing = False

    def reconfigure(self) -> None:
        settings = self.settings_manager.get_settings()
        video_opts = 0
        if settings.video_settings.full_screen:
            video_opts |= pygame.FULLSCREEN
            if settings.video_settings.hardware_accel:
                video_opts |= pygame.HWSURFACE
            elif settings.video_settings.open_gl:
                video_opts |= pygame.OPENGL
        if settings.video_settings.double_buffer:
            video_opts |= pygame.DOUBLEBUF

        self.game_input.reconfigure(settings)
        self.scene.reconfigure(settings)
        self.frame_rate = settings.video_settings.frame_rate
        self.screen = pygame.display.set_mode(
            size=settings.video_settings.resolution,
            flags=video_opts)

    def do_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            self.game_input.process_event(event)
            self.scene.process_event(event)

    def do_update(self, frame_delta: int) -> None:
        self.scene.update(frame_delta)

        # This needs to happen last.
        self.game_input.update(frame_delta)

    def do_render(self) -> None:
        self.scene.render(self.screen)

    def __init__(
        self,
        clock: pygame.time.Clock,
        game_input: IGameInput,
        settings_manager: ISettingManager,
    ) -> None:
        self.is_playing: bool = False
        self.scene: Optional[IGameScene] = None
        self.screen: Optional[pygame.Surface] = None
        self.frame_rate: int = 0
        self.clock = clock
        self.game_input = game_input
        self.settings_manager = settings_manager
