from typing import Dict, Tuple
from pytmx import TiledMap, TiledTileLayer, TiledTileset

from pygame import Surface

from malibu_lib.typing import IGameSprite, IGameItem


class MapTileSprite(IGameSprite):

    _position: Tuple[float, float]
    _image: Surface
    _tiledmap: TiledMap

    @property
    def position(self) -> Tuple[float, float]:
        return self._position

    @position.setter
    def position(self, value: Tuple[float, float]) -> None:
        self._position = value

    @property
    def inventory(self) -> Dict[str, IGameItem]:
        raise NotImplementedError()

    @property
    def image(self) -> Surface:
        return self._image

    @property
    def rect(self) -> Surface:
        rect = self._image.get_rect()
        rect.midbottom = self.position
        return rect

    def execute(self, action: str, *args, **kwargs) -> bool:
        pass

    def update(self, frame_delta: int) -> None:
        pass

    def initialize(self, **kwargs) -> None:
        x, y = kwargs.get("position", (0, 0))
        # Adjust the location to compensate for the
        # map editors coordinate system
        self._position = (x + 8, y + 16)
        self._image = kwargs["tile"]
