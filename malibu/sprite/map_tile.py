from pygame import Surface

from malibu_lib.abc import GameSprite


class MapTileSprite(GameSprite):
    @property
    def image(self) -> Surface:
        pass

    @property
    def rect(self) -> Surface:
        pass

    def update(self, frame_delta: int) -> None:
        pass

    def initialize(self, **kwargs) -> None:
        pass
