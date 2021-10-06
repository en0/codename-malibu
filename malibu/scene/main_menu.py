import pygame
from pygame import Surface, draw
from pytmx import load_pygame, TiledMap, TiledTileLayer

from malibu_lib.abc import SceneABC
from malibu_lib.model import GameSettings
from malibu_lib.typing import IGameInput, IGameSprite

from ..sprite import *


class MainMenuScene(SceneABC):

    _tm: TiledMap
    _player: IGameSprite
    _campfire: IGameSprite
    _chest: IGameSprite

    def startup(self) -> None:
        self._tm = load_pygame("malibu/assets/world/demo.tmx")
        self._player = self.create_sprite(SPRITE_PLAYER, position=(100, 100))
        for x in self._tm.objects:
            if x.type == "campfire":
                self._campfire = self.create_sprite(SPRITE_CAMPFIRE, position=(x.x, x.y))
            elif x.type == "chest":
                self._chest = self.create_sprite(SPRITE_CHEST, position=(x.x, x.y))

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

        screen.blit(self._player.image, self._player.rect)
        screen.blit(self._campfire.image, self._campfire.rect)
        screen.blit(self._chest.image, self._chest.rect)

    def update(self, frame_delta: int) -> None:
        self._player.update(frame_delta)
        self._campfire.update(frame_delta)
        self._chest.update(frame_delta)

        # Should we use the command pattern?
        # I also need a common interface for sprites.
        # how would one lite a fire?  is it a generic action?
        if self.game_input.is_triggered("inventory"):
            self._chest.toggle()
            self._campfire.lite()
