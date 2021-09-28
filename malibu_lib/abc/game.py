import pygame
from typing import Optional
from abc import abstractmethod

from ..utils import auto_wireup_events
from ..model import GameSettings
from ..events import *
from ..typing import (
    IEventBus,
    IGame,
    IGameInput,
    IGameScene,
    ISettingManager,
)


class GameABC(IGame):

    @abstractmethod
    def update(self, frame_delta: int) -> None:
        ...

    @abstractmethod
    def startup(self) -> None:
        ...

    @abstractmethod
    def shutdown(self) -> None:
        ...

    @property
    def game_input(self) -> IGameInput:
        return self._game_input

    @property
    def settings_manager(self) -> ISettingManager:
        return self._settings_manager

    @property
    def screen(self) -> pygame.Surface:
        return self._screen

    @property
    def scene(self) -> Optional[IGameScene]:
        return self._scene

    def set_scene(self, next_scene: IGameScene) -> None:
        if self._scene: self._scene.shutdown()
        self._scene = next_scene
        self._scene.startup()

    def close(self) -> None:
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def play(self) -> None:
        self._is_playing = True
        self.startup()
        while self._is_playing:
            delta = self._clock.tick(self._frame_rate)

            # Process game events
            for event in pygame.event.get():
                self._ebus.process_event(event)
                self._game_input.process_event(event)
                self._scene.process_event(event)

            # Process game updates
            self._scene.update(delta)
            self.update(delta)
            self._game_input.update(delta)

            # Update Screen
            self._screen.fill((0, 0, 66))
            self._scene.render(self._screen)
            pygame.display.flip()

        self.shutdown()
        pygame.quit()

    def _on_settings_changed(self, event: pygame.event.Event) -> None:
        self._reconfigure(event.settings)

    def _on_game_exit(self, event: pygame.event.Event) -> None:
        self._is_playing = False

    def _initialize(self) -> None:
        settings = self._settings_manager.get_settings()
        self._reconfigure(settings)

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
        self._screen = pygame.display.set_mode(
            size=settings.video_settings.resolution,
            flags=video_opts)

    def __init__(
        self,
        ebus: IEventBus,
        clock: pygame.time.Clock,
        game_input: IGameInput,
        settings_manager: ISettingManager,
    ) -> None:
        self._is_playing: bool = False
        self._scene: Optional[IGameScene] = None
        self._screen: Optional[pygame.Surface] = None
        self._frame_rate: int = 0
        self._clock = clock
        self._game_input = game_input
        self._settings_manager = settings_manager
        self._ebus = ebus

        # initialize the screen
        self._initialize()

        # Wireup events
        self._ebus.attach(SETTINGS_CHANGED, self._on_settings_changed)
        self._ebus.attach(GAME_EXIT, self._on_game_exit)
        auto_wireup_events(self._ebus, self)
