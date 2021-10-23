from pygame import Surface, display, Rect, Vector2, FULLSCREEN, HWACCEL, DOUBLEBUF
from typing import Union, Tuple

from ..const import SCREEN_SIZE
from ..typing import IGfxService


class GraphicsService(IGfxService):

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
        dest = absolute if relative is None else self._compute_absolute(relative)
        self.hw_surface.blit(source, dest)

    def get_world_boundary(self) -> Rect:
        return self.world_boundary.copy()

    def set_world_boundary(self, rect: Rect) -> None:
        self.world_boundary = rect.copy()

    def get_viewport(self) -> Rect:
        return self.viewport.copy()

    def set_focus(self, point: Union[Vector2, Tuple[float, float]]) -> None:
        self.viewport.center = point

    def get_hw_surface(self) -> Surface:
        return self.hw_surface

    def initialize(self) -> None:
        self.hw_surface = display.set_mode(SCREEN_SIZE, HWACCEL | DOUBLEBUF)
        self.viewport = self.hw_surface.get_rect()
        self.world_boundary = self.viewport.copy()
        self.world_offset = 0, 0

    def _compute_absolute(
        self,
        rel: Union[Rect, Vector2, Tuple[float, float]]
    ) -> Tuple[float, float]:
        ...
