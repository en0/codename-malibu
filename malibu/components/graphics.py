import pygame

from .base import GameComponentBase, SubMap_T
from ..enum import ComponentMessageEnum
from ..typing import IGraphicsComponent, IWorldMap, IGraphicsService


class TestGraphicsComponent(GameComponentBase, IGraphicsComponent):

    subscriptions = [
        ComponentMessageEnum.SET_LOCATION
    ]

    def set_location(self, sender: object, value: pygame.Vector2):
        self.rect.center = value

    def render(self, gfx: IGraphicsService):
        #gfx.blit(self.sprite, self.rect)
        surface = gfx.get_hw_surface()
        abs_center = gfx.compute_absolute(self.rect.center)
        abs_rect = gfx.compute_absolute_rect(self.rect)
        pygame.draw.circle(surface, (0, 0, 200), abs_center, 10)
        pygame.draw.rect(gfx.get_hw_surface(), (200, 0, 0), abs_rect, width=1)

    def __init__(self):
        self.rect = pygame.Rect(0, 0, 10, 10)
        #self.sprite = pygame.Surface((20, 20))
        #self.rect = self.sprite.get_rect()

        #self.sprite.set_colorkey((255, 0, 255))
        #self.sprite.fill((255, 0, 255))
        #pygame.draw.circle(self.sprite, (0, 0, 200), (10, 10), 10)
        #pygame.draw.rect(self.sprite, (200, 0, 0), pygame.Rect(0, 0, 20, 20), width=1)
