from pygame import Vector2, Rect
from typing import Optional
from .base import GameComponentBase
from ..typing import ISpatialComponent
from ..enum import GameObjectMessageEnum, DirectionEnum


class SpatialComponent(GameComponentBase, ISpatialComponent):

    subscriptions = [
        GameObjectMessageEnum.SET_LOCATION,
        GameObjectMessageEnum.SET_FOOTPRINT,
        GameObjectMessageEnum.SET_BOUNDING_BOX,
        GameObjectMessageEnum.SET_FACING_DIR,
    ]

    _location: Optional[Vector2] = None
    _footprint: Optional[Rect] = None
    _bounding_box: Optional[Rect] = None
    _facing: Optional[DirectionEnum] = None

    def on_set_location(self, sender: object, value: Vector2) -> None:
        self._location = value

    def on_set_footprint(self, sender: object, value: Rect) -> None:
        self._footprint = value

    def on_set_bounding_box(self, sender: object, value: Rect) -> None:
        self._bounding_box = value

    def on_set_facing_dir(self, sender: object, value: DirectionEnum) -> None:
        self._facing = value

    def get_location(self) -> Optional[Vector2]:
        return self._location

    def get_footprint(self) -> Optional[Rect]:
        return self._footprint

    def get_bounding_box(self) -> Optional[Rect]:
        return self._bounding_box

    def get_facing_direction(self) -> Optional[DirectionEnum]:
        return self._facing

    def set_location(self, value: Vector2) -> None:
        self._location = value
        self.parent.receive_message(
            sender=self,
            msg_type=GameObjectMessageEnum.SET_LOCATION,
            value=value)

    def set_footprint(self, value: Rect) -> None:
        self._footprint = value
        self.parent.receive_message(
            sender=self,
            msg_type=GameObjectMessageEnum.SET_FOOTPRINT,
            value=value)

    def set_bounding_box(self, value: Rect) -> None:
        self._bounding_box = value
        self.parent.receive_message(
            sender=self,
            msg_type=GameObjectMessageEnum.SET_BOUNDING_BOX,
            value=value)

    def set_facing_direction(self, value: DirectionEnum) -> None:
        self._facing = value
        self.parent.receive_message(
            sender=self,
            msg_type=GameObjectMessageEnum.SET_FACING_DIR,
            value=value)

