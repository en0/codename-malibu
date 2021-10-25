import pygame

from .sandbox import SceneSandbox
from ..enum import SceneEnum
from ..typing import IGameScene


class GameMenu(SceneSandbox, IGameScene):

    _rect: pygame.Surface = None
    _suf: pygame.Surface = None

    def activate(self) -> None:
        font = pygame.font.SysFont(pygame.font.get_default_font(), 45)
        self._suf = font.render("GAME MENU", True, (0, 0, 0), (255, 255, 255))
        self._rect = self._suf.get_rect()
        self._rect.center = pygame.Rect(0, 0, *self.graphics.get_resolution()).center

    def inactivate(self) -> None:
        pass

    def update(self, frame_delta: float) -> None:
        if self.keyboard.is_pressed(pygame.K_ESCAPE):
            self.pop_to_scene()
        #self._scene.render()
        self.graphics.blit(self._suf, absolute=self._rect)

    def __init__(self, current_scene: IGameScene) -> None:
        self._scene = current_scene
