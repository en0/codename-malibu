import pygame
from pygame import Surface, draw
from pytmx import load_pygame, TiledMap, TiledTileLayer

from malibu_lib.abc import SceneABC
from malibu_lib.model import GameSettings
from malibu_lib.typing import IGameInput


class MainMenuScene(SceneABC):

    _tm: TiledMap

    def startup(self) -> None:
        self._tm = load_pygame("malibu/assets/world/demo.tmx")

    def shutdown(self) -> None:
        ...

    def render(self, screen: Surface) -> None:
        screen.fill(self._tm.background_color or (0, 0, 0))
        for layer in self._tm.visible_layers:
            if isinstance(layer, TiledTileLayer):
                for x, y, gid in layer:
                    tile = self._tm.get_tile_image_by_gid(gid)
                    if not tile:
                        continue
                    screen.blit(tile, (x * self._tm.tilewidth, y * self._tm.tileheight))


    def update(self, frame_delta: int) -> None:
        ...
