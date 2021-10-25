import pygame

from .base import GameComponentBase, SubMap_T
from ..enum import GameObjectMessageEnum
from ..typing import IGraphicsComponent, IWorldMap, IGraphicsService


class TestGraphicsComponent(GameComponentBase, IGraphicsComponent):

    subscriptions = [
        GameObjectMessageEnum.SET_LOCATION
    ]

    def on_set_location(self, sender: object, value: pygame.Vector2):
        self.rect.center = value

    def render(self, gfx: IGraphicsService):
        surface = gfx.get_hw_surface()
        abs_center = gfx.compute_absolute(self.rect.center)
        abs_rect = gfx.compute_absolute_rect(self.rect)
        pygame.draw.circle(surface, (0, 0, 200), abs_center, 10)
        pygame.draw.rect(gfx.get_hw_surface(), (200, 0, 0), abs_rect, width=1)

    def __init__(self):
        self.rect = pygame.Rect(0, 0, 10, 10)
