from pygame import Surface, draw

from .component_base import ComponentBase
from ..typing import IGraphicsComponent, IGraphicsService
from ..enum import StateEnum


class RenderSprite(ComponentBase, IGraphicsComponent):

    def render(self, gfx: IGraphicsService):
        sprite = self.get_state(StateEnum.SPRITE)
        location = self.get_state(StateEnum.SPRITE_LOCATION)
        if sprite and location is not None:
            gfx.blit(sprite, location)

            if self._debug:
                bounding_box = self.get_state(StateEnum.BOUNDING_BOX)
                footprint = self.get_state(StateEnum.FOOTPRINT)
                draw.rect(gfx.get_hw_surface(), (0, 0, 255), gfx.compute_absolute_rect(bounding_box), width=1)
                draw.rect(gfx.get_hw_surface(), (255, 0, 0), gfx.compute_absolute_rect(footprint), width=1)

    def __init__(self, debug=False):
        self._debug = debug