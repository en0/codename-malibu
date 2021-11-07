from pygame import Rect, Surface, draw, Vector2
from ..typing import IBehaviorComponent, IGameObject, IWorldMap


class StaticSpriteComponent(IBehaviorComponent):

    parent: IGameObject

    @property
    def sprite(self) -> Surface:
        return self.parent.data.sprite

    @sprite.setter
    def sprite(self, value: Surface) -> None:
        self.parent.data.sprite = value

    @property
    def footprint(self) -> Rect:
        return self.parent.data.footprint

    @footprint.setter
    def footprint(self, value: Rect) -> None:
        self.parent.data.footprint = value

    @property
    def bounding_box(self) -> Rect:
        return self.parent.data.bounding_box

    @bounding_box.setter
    def bounding_box(self, value: Rect) -> None:
        self.parent.data.bounding_box = value

    def set_parent(self, game_object: IGameObject) -> None:
        self.parent = game_object
        self._initialize_sprite()

    def update(self, frame_delta: float, world: IWorldMap):
        pass

    def _initialize_sprite(self):
        self.footprint = Rect(0, 0, 45, 20)
        self.bounding_box = Rect(0, 0, 45, 120)
        self.sprite = Surface(self.bounding_box.size)
        self.footprint.midbottom = self.bounding_box.midbottom
        self.sprite.fill((0, 0, 255))
        draw.rect(self.sprite, (255, 0, 0), self.footprint,  width=1)

    def __init__(self):
        self.rect = Rect(0, 0, 10, 10)
