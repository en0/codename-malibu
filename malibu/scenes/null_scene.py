import pygame
from ..mixins import SpriteFactoryMixin, KeyboardMixin, GraphicMixin

from ..typing import IGameScene, IGameObject


class NullScene(SpriteFactoryMixin, KeyboardMixin, GraphicMixin, IGameScene):

    @property
    def player_location(self) -> pygame.Vector2:
        return pygame.Vector2(0)

    def activate(self) -> None:
        pass

    def inactivate(self) -> None:
        pass

    def process_inputs(self) -> None:
        pass

    def update(self, frame_delta: float) -> None:
        pass

    def render(self) -> None:
        pass

    def __init__(self) -> None:
        pass
