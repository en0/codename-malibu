from pygame import Rect, Vector2


class Camera:

    @property
    def world_offset(self):
        return self._world_offset

    @property
    def aperture(self) -> Rect:
        return self._aperture

    def set_focus(self, location: Vector2):
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
