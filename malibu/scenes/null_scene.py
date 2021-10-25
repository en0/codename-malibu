import pygame
from ..mixins import ObjectFactoryMixin, KeyboardMixin, GraphicMixin

from ..typing import IGameScene, IGameObject


class NullScene(ObjectFactoryMixin, KeyboardMixin, GraphicMixin, IGameScene):

    def activate(self) -> None:
        pass

    def inactivate(self) -> None:
        pass

    def update(self, frame_delta: float) -> None:
        pass
