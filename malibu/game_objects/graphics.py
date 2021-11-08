from pygame import Rect
from pygame import Surface

from ..typing import IGraphicsComponent, IGameObject
from ..enum import StateEnum


class DefaultGraphicsComponent(IGraphicsComponent):

    parent: IGameObject

    def set_parent(self, game_object: IGameObject):
        self.parent = game_object

    def render(self, gfx: Surface):
        sprite = self.parent.get_state(StateEnum.SPRITE)
        location = self.parent.get_state(StateEnum.SPRITE_LOCATION)
        if sprite and location is not None:
            gfx.blit(sprite, location)

