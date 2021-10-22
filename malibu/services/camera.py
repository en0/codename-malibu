from pygame import Rect, Vector2

from .locator import ServiceLocator
from ..enum import CameraTypeEnum, ComponentMessageEnum
from ..typing import ICamera, ICameraFactory, IGameObject


class CameraFactory(ICameraFactory):
    def create_camera(self, world: Rect = None):
        aperture = ServiceLocator.get_graphics().get_rect()
        if world == None:
            return StaticCamera(aperture)
        else:
            return Camera(aperture, world)


class Camera(ICamera):

    @property
    def world_offset(self):
        return self._world_offset

    @property
    def aperture(self) -> Rect:
        return self._aperture

    def attach_to(self, obj: IGameObject) -> None:
        obj.subscribe(ComponentMessageEnum.SET_LOCATION, self)

    def receive_message(self, sender: object, msg_type: ComponentMessageEnum, value: any):
        self._set_focus(value)

    def _set_focus(self, location: Vector2):
        self._aperture.center = location
        self._aperture.x = max(self._aperture.x, self._world.x)
        self._aperture.y = max(self._aperture.y, self._world.y)
        self._aperture.right = min(self._aperture.right, self._world.right)
        self._aperture.bottom = min(self._aperture.bottom, self._world.bottom)
        self._world_offset = -self._aperture.x, -self._aperture.y

    def __init__(self, aperture: Rect, world: Rect):
        self._aperture = aperture
        self._world = world
        self._world_offset = 0, 0


class StaticCamera(ICamera):

    @property
    def world_offset(self):
        return 0

    @property
    def aperture(self) -> Rect:
        return _aperture

    def attach_to(self, obj: IGameObject) -> None:
        pass

    def receive_message(self, sender: object, msg_type: ComponentMessageEnum, value: any):
        pass

    def __init__(self, aperture: Rect):
        self._apreture = aperture
