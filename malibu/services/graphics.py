from pygame import Surface, display, Rect, Vector2, FULLSCREEN, HWACCEL, DOUBLEBUF
from typing import Union, Tuple, Optional

from ..enum import ComponentMessageEnum
from ..const import SCREEN_SIZE
from ..typing import IGraphicsService, IGameObject, INotifiableObject


class GraphicsService(INotifiableObject, IGraphicsService):

    hw_surface: Surface
    world_boundary: Surface
    viewport: Rect
    world_offset: Tuple[float, float]

    def blit(
        self,
        source: Surface,
        relative: Union[Rect, Vector2, Tuple[float, float]] = None,
        absolute: Union[Rect, Vector2, Tuple[float, float]] = None,
    ) -> None:
        dest = absolute if relative is None else self.compute_absolute(relative)
        self.hw_surface.blit(source, dest)

    def fill(self, color: Tuple[int, int, int], rect: Optional[Rect] = None) -> None:
        self.hw_surface.fill(color, rect)

    def attach(self, obj: IGameObject) -> None:
        obj.subscribe(ComponentMessageEnum.SET_LOCATION, self)

    def detach(self, obj: IGameObject) -> None:
        obj.unsubscribe(ComponentMessageEnum.SET_LOCATION, self)

    def receive_message(self, sender: object, msg_type: ComponentMessageEnum, value: any):
        self._set_focus(value)

    def get_world_boundary(self) -> Rect:
        return self.world_boundary.copy()

    def set_world_boundary(self, rect: Rect) -> None:
        self.world_boundary = rect.copy()

    def get_viewport(self) -> Rect:
        return self.viewport.copy()

    def get_resolution(self) -> Tuple[int, int]:
        return self.hw_surface.get_rect().size

    def set_focus(self, point: Union[Vector2, Tuple[float, float]]) -> None:
        self._set_focus(point)

    def get_hw_surface(self) -> Surface:
        return self.hw_surface

    def initialize(self) -> None:
        self.hw_surface = display.set_mode(SCREEN_SIZE, HWACCEL | DOUBLEBUF)
        self.viewport = self.hw_surface.get_rect()
        self.world_boundary = self.viewport.copy()
        self.world_offset = 0, 0

    def compute_absolute(
        self,
        rel: Union[Rect, Vector2, Tuple[float, float]]
    ) -> Tuple[float, float]:
        x, y, *_ = rel
        return x + self.world_offset[0], y + self.world_offset[1]

    def compute_absolute_vector(self, rel: Vector2) -> Vector2:
        return Vector2(self.compute_absolute(rel))

    def compute_absolute_rect(self, rel: Rect) -> Rect:
        ret = rel.copy()
        ret.topleft = self.compute_absolute(rel)
        return ret

    def _set_focus(self, value: Vector2) -> None:
        self.viewport.center = value
        self.viewport.x = max(self.viewport.x, self.world_boundary.x)
        self.viewport.y = max(self.viewport.y, self.world_boundary.y)
        self.viewport.right = min(self.viewport.right, self.world_boundary.right)
        self.viewport.bottom = min(self.viewport.bottom, self.world_boundary.bottom)
        self.world_offset = -self.viewport.x, -self.viewport.y
