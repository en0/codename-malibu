import pygame

from .sandbox import SceneSandbox
from ..enum import SceneEnum
from ..typing import IGameScene


class GameMenu(SceneSandbox, IGameScene):

    _suf: pygame.Surface = None

    @property
    def player_location(self) -> pygame.Vector2:
        return self.graphics.get_rect().center

    def activate(self) -> None:
        font = pygame.font.SysFont(pygame.font.get_default_font(), 45)
        self._suf = font.render("GAME MENU", True, (0, 0, 0), (255, 255, 255))

    def inactivate(self) -> None:
        pass

    def process_inputs(self) -> None:
        if self.keyboard.is_pressed(pygame.K_ESCAPE):
            self.pop_to_scene()

    def update(self, frame_delta: float) -> None:
        pass

    def render(self) -> None:
        self._scene.render()
        rect = self._suf.get_rect()
        rect.center = self.player_location
        self.graphics.blit(self._suf, rect)

    def __init__(self, current_scene: IGameScene) -> None:
        self._scene = current_scene
