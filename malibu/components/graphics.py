import pygame

from .base import GameComponentBase, SubMap_T
from ..enum import ComponentMessageEnum
from ..typing import IGraphicsComponent, IWorldMap


class TestGraphicsComponent(GameComponentBase, IGraphicsComponent):

    subscriptions = [
        ComponentMessageEnum.SET_LOCATION
    ]

    rect = pygame.Rect(0, 0, 10, 10)

    def set_location(self, sender: object, value: pygame.Vector2):
        self.rect.center = value

    def render(self, gfx: pygame.Surface):
        pygame.draw.circle(gfx, (0, 0, 200), self.rect.center, 10)
        pygame.draw.rect(gfx, (200, 0, 0), self.rect, width=1)

