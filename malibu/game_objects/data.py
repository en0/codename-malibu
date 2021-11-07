from pygame import Vector2, Rect, Surface
from typing import Optional
from ..typing import IDataComponent
from ..enum import GameObjectMessageEnum, DirectionEnum


class DataComponent(IDataComponent):

    _sprite: Optional[Surface] = None
    _facing_direction: Optional[DirectionEnum] = None
    _bounding_box: Optional[Rect] = None
    _footprint: Optional[Rect] = None
    _location: Optional[Vector2] = None
    _transform: Vector2 = Vector2(0)
    _spec_bounding_box: Rect = None
    _spec_footprint: Rect = None

    @property
    def location(self) -> Optional[Vector2]:
        return self._location

    @location.setter
    def location(self, value: Vector2) -> None:
        self._location = value
        self._recompute_spacial()

    @property
    def footprint(self) -> Optional[Rect]:
        return self._footprint

    @property
    def bounding_box(self) -> Optional[Rect]:
        return self._bounding_box

    @property
    def facing_direction(self) -> Optional[DirectionEnum]:
        return self._facing_direction

    @facing_direction.setter
    def facing_direction(self, value: DirectionEnum) -> None:
        self._facing_direction = value

    @property
    def sprite(self) -> Optional[Surface]:
        return self._sprite

    @sprite.setter
    def sprite(self, value: Surface) -> None:
        self._sprite = value

    @property
    def transform(self) -> Vector2:
        return self._transform

    @transform.setter
    def transform(self, value: Vector2) -> None:
        self._transform = value

    def set_spacial(self, bounding_box: Rect, footprint: Rect = None):
        self._spec_bounding_box = bounding_box
        self._spec_footprint = footprint
        self._recompute_spacial()

    def _recompute_spacial(self):
        if not self.location or not self._spec_bounding_box or not self._spec_footprint:
            return
        bounding_box = self._spec_bounding_box.copy()
        footprint = self._spec_footprint.copy()
        footprint.center = self.location
        offset = Vector2(self._spec_bounding_box.topleft) - Vector2(self._spec_footprint.topleft)
        bounding_box.topleft = Vector2(self.footprint.topleft) - offset
        self._bounding_box = bounding_box
        self._footprint = footprint