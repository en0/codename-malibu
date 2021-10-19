import pygame
from collections import deque
from typing import Optional

from ..const import FRAME_RATE
from ..typing import IGameScene, IGameService
from ..mixins import (
    LoggerMixin,
    KeyboardMixin,
    AudioMixin,
    GraphicMixin,
)


class GameService(LoggerMixin, KeyboardMixin, AudioMixin, GraphicMixin, IGameService):

    @property
    def target_frame_rate(self) -> int:
        return FRAME_RATE

    def close(self) -> None:
        self._is_stopping = True

    def set_scene(self, scene: IGameScene) -> None:
        self._next_scene = scene

    def run(self, scene: IGameScene):


        font_name =  pygame.font.get_default_font()
        self._fnt = pygame.font.SysFont(font_name, 24)
        frame_delta = self._tick()

        self._scene = scene
        self._scene.activate()

        while not self._is_stopping:

            self._is_stopping = bool(pygame.event.get(pygame.QUIT))

            # Process input
            events = pygame.event.get()
            self.keyboard.update(events)
            self._scene.process_inputs()

            # Update game
            self._scene.update(frame_delta)

            # Render
            self._scene.render()
            self._show_framerate()
            self.audio.update(self._scene.player_location)
            pygame.display.flip()

            if self._next_scene:
                self._flip_scene()

            frame_delta = self._tick()

            if frame_delta >= 0.05:
                self.log.critical("Slow frame detected: System cannot keep up!")

    def _tick(self):
        return self._clock.tick(FRAME_RATE) / 1000.0

    def _flip_scene(self):
        self.log.info(
            "Scene Transition: %s -> %s",
            self._scene.__class__.__name__,
            self._next_scene.__class__.__name__)

        self._scene = self._next_scene
        self._next_scene = None
        self._scene.activate()

    def _show_framerate(self):
        fr = self._clock.get_fps()
        self._fr_min = min(self._fr_min, fr)
        self._fr_max = max(self._fr_max, fr)
        self.graphics.blit(self._fnt.render(
            f"FPS: {fr:.2f} MIN={self._fr_min:.2f} MAX={self._fr_max:.2f}",
            True,
            (255, 0, 0),
            (0, 0, 0)
        ), (0, 0))
        self._cnt = (self._cnt + 1) % 1000
        if self._cnt == 0:
            self._fr_max = 0
            self._fr_min = FRAME_RATE
            self._cnt = 0

    def __init__(self):
        self._clock = pygame.time.Clock()
        self._is_stopping = False
        self._scene: Optional[IGameScene] = None
        self._next_scene: Optional[IGameScene] = None
        self._fr_min = FRAME_RATE
        self._fr_max = 0
        self._fnt = None
        self._cnt = 0
