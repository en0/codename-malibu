from pygame import Rect
from pygame import Surface

from ..typing import IGraphicsComponent, IWorldMap, IGameObject, IBehaviorComponent


class DefaultGraphicsComponent(IGraphicsComponent):

    parent: IGameObject

    def get_location_rect(self) -> Rect:
        bb = self.parent.data.bounding_box.copy()
        fp = self.parent.data.footprint.copy()
        fp.center = self.parent.data.location
        bb.midbottom = fp.midbottom
        return bb

    def set_parent(self, game_object: IGameObject):
        self.parent = game_object

    def render(self, gfx: Surface):
        if self.parent.data.sprite and self.parent.data.location:
            gfx.blit(self.parent.data.sprite, self.get_location_rect())
