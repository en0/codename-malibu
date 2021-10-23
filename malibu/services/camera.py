from pygame import Rect, Vector2
from typing import Tuple

from .locator import ServiceLocator
from ..enum import ComponentMessageEnum
from ..typing import ICamera, IGameObject


class Camera(ICamera):

    _aperture: Rect
    _world: Rect
    _world_offset: Tuple[float, float]

    @property
    def world_offset(self):
        return self._world_offset

    @property
    def aperture(self) -> Rect:
        return self._aperture

    def set_world_rect(self, rect: Rect) -> None:
        self._world = rect.copy()

    def attach(self, obj: IGameObject) -> None:
        obj.subscribe(ComponentMessageEnum.SET_LOCATION, self)

    def detach(self, obj: IGameObject) -> None:
        obj.unsubscribe(ComponentMessageEnum.SET_LOCATION, self)

    def receive_message(self, sender: object, msg_type: ComponentMessageEnum, value: any) -> None:
        self._set_focus(value)

    def _set_focus(self, location: Vector2):
        self._aperture.center = location
        self._aperture.x = max(self._aperture.x, self._world.x)
        self._aperture.y = max(self._aperture.y, self._world.y)
        self._aperture.right = min(self._aperture.right, self._world.right)
        self._aperture.bottom = min(self._aperture.bottom, self._world.bottom)
        self._world_offset = -self._aperture.x, -self._aperture.y

    def initialize(self):
        self._aperture = ServiceLocator.get_graphics().get_rect()
        self._world = self._aperture.copy()
        self._world_offset = 0, 0

