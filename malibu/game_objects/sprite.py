from pygame import Rect, Surface, draw, Vector2

from ..typing import IBehaviorComponent, IGameObject, IWorldMap
from ..enum import StateEnum, GameObjectMessageEnum
from ..mixins import NotifiableMixin


class StaticSpriteComponent(IBehaviorComponent, NotifiableMixin):

    parent: IGameObject

    @property
    def sprite(self) -> Surface:
        return self.parent.get_state(StateEnum.SPRITE)

    @sprite.setter
    def sprite(self, value: Surface) -> None:
        self.parent.set_state(StateEnum.SPRITE, value)

    @property
    def footprint(self) -> Rect:
        return self.parent.get_state(StateEnum.FOOTPRINT)

    @footprint.setter
    def footprint(self, value: Rect) -> None:
        self.parent.set_state(StateEnum.FOOTPRINT, value)

    @property
    def bounding_box(self) -> Rect:
        return self.parent.get_state(StateEnum.BOUNDING_BOX)

    @bounding_box.setter
    def bounding_box(self, value: Rect) -> None:
        self.parent.set_state(StateEnum.BOUNDING_BOX, value)

    def set_parent(self, game_object: IGameObject) -> None:
        self.parent = game_object
        self._initialize_sprite()
        self.subscribe(game_object, [
            GameObjectMessageEnum.STATE_CHANGED,
        ])

    def update(self, frame_delta: float, world: IWorldMap):
        ...

    def on_state_changed(self, sender: object, key: StateEnum):
        if key != StateEnum.WORLD_LOCATION:
            return
        delta = Vector2(self._rel_footprint.topleft) - Vector2(self._rel_bounding_box.topleft)
        footprint = self._rel_footprint.copy()
        footprint.center = self.parent.get_state(StateEnum.WORLD_LOCATION)
        bounding_box = self._rel_bounding_box.copy()
        bounding_box.topleft = Vector2(footprint.topleft) - delta
        self.parent.set_state(StateEnum.FOOTPRINT, footprint)
        self.parent.set_state(StateEnum.BOUNDING_BOX, bounding_box)
        self.parent.set_state(StateEnum.SPRITE_LOCATION, bounding_box.topleft)

    def _initialize_sprite(self):
        self._rel_footprint = Rect(0, 0, 45, 20)
        self._rel_bounding_box = Rect(0, 0, 45, 120)
        self._sprite = Surface(self._rel_bounding_box.size)
        self._rel_footprint.midbottom = self._rel_bounding_box.midbottom
        self._sprite.fill((0, 0, 255))
        draw.rect(self._sprite, (255, 0, 0), self._rel_footprint,  width=1)

        self.parent.set_state(StateEnum.SPRITE, self._sprite)

    def __init__(self):
        self.rect = Rect(0, 0, 10, 10)
