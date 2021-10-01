import pygame
from typing import Optional

from ..mixin import EventListenerMixin
from ..model import GameSettings
from ..typing import (
    IGame,
    IGameInput,
    IGameScene,
    ISettingManager,
    IGameSceneFactory,
)


class GameABC(EventListenerMixin, IGame):

    @property
    def settings_manager(self) -> ISettingManager:
        return self._settings_manager

    @property
    def game_input(self) -> IGameInput:
        return self._game_input

    def set_scene(self, next_scene: str) -> None:
        if self._scene:
            self._scene.shutdown()
        self._scene = self._scene_factory(next_scene)
        self._scene.startup()

    def close(self) -> None:
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def play(self) -> None:

        settings = self._settings_manager.get_settings()
        self._reconfigure(settings)

        self._is_playing = True
        self.startup()
        while self._is_playing:
            delta = self._clock.tick(self._frame_rate)

            # Process game events
            for event in pygame.event.get():
                self._game_input.process_event(event)
                self._scene.process_event(event)
                self.process_event(event)

            # Process game updates
            self._scene.update(delta)
            self.update(delta)
            self._game_input.update(delta)

            # Update Screen
            self._scene.render(self._screen)
            screen = pygame.transform.scale(self._screen, self._display.get_size())
            self._display.blit(screen, (0, 0))
            pygame.display.flip()

        self.shutdown()
        pygame.quit()

    def on_settings_changed(self, event: pygame.event.Event) -> None:
        self._reconfigure(event.settings)

    def on_quit(self, event: pygame.event.Event) -> None:
        self._is_playing = False

    def _reconfigure(self, settings: GameSettings) -> None:
        video_opts = 0
        if settings.video_settings.full_screen:
            video_opts |= pygame.FULLSCREEN
            if settings.video_settings.hardware_accel:
                video_opts |= pygame.HWSURFACE
            elif settings.video_settings.open_gl:
                video_opts |= pygame.OPENGL
        if settings.video_settings.double_buffer:
            video_opts |= pygame.DOUBLEBUF

        self._frame_rate = settings.video_settings.frame_rate
        self._screen = pygame.Surface(settings.video_settings.viewport)
        self._display = pygame.display.set_mode(
            size=settings.video_settings.resolution,
            flags=video_opts
        )

    def __init__(
        self,
        clock: pygame.time.Clock,
        game_input: IGameInput,
        settings_manager: ISettingManager,
        scene_factory: IGameSceneFactory,
    ) -> None:
        self._is_playing: bool = False
        self._scene: Optional[IGameScene] = None
        self._display: Optional[pygame.Surface] = None
        self._screen: Optional[pygame.Surface] = None
        self._frame_rate: int = 0
        self._clock = clock
        self._game_input = game_input
        self._settings_manager = settings_manager
        self._scene_factory = scene_factory
