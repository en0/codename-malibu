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
        body_rect = pygame.Rect(0, 0, 45, 120)
        foot_rect = pygame.Rect(0, 0, 45, 20)
        foot_rect.center = gfx.compute_absolute(self.rect.center)
        body_rect.midbottom = foot_rect.midbottom

        pygame.draw.rect(gfx.get_hw_surface(), (0, 0, 255), body_rect)
        pygame.draw.rect(gfx.get_hw_surface(), (255, 0, 0), foot_rect, width=2)

    def __init__(self):
        self.rect = pygame.Rect(0, 0, 10, 10)
