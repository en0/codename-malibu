import pygame
from pygame import Surface
from pytmx import load_pygame, TiledMap, TiledTileLayer
from typing import List

from malibu_lib.abc import SceneABC
from malibu_lib.typing import IGameSprite

from .. import kb
from ..sprite import *


class MainMenuScene(SceneABC):

    _tm: TiledMap
    _player: IGameSprite
    _sprites: List[IGameSprite]
    _background: List[IGameSprite]
    _foreground: List[IGameSprite]

    def startup(self) -> None:
        self._background = []
        self._foreground = []
        self._tm = load_pygame("malibu/assets/world/demo.tmx")
        self._player = self.create_sprite(SPRITE_PLAYER, position=(100, 100))
        self._sprites = [self.create_sprite(x.type, position=(x.x, x.y)) for x in self._tm.objects]
        for layer in self._tm.visible_layers:
            if not isinstance(layer, TiledTileLayer):
                continue
            for x, y, gid in layer:
                tile = self._tm.get_tile_image_by_gid(gid)
                if not tile:
                    continue
                tile_sprite = self.create_sprite(
                    SPRITE_MAP_TILE,
                    tile=tile,
                    position=(x * self._tm.tilewidth, y * self._tm.tileheight),
                    propertie=self._tm.get_tile_properties_by_gid(gid),
                )
                {
                    'background': self._background,
                    'foreground': self._foreground,
                }[layer.properties["layer"]].append(tile_sprite)

    def shutdown(self) -> None:
        ...

    def render(self, screen: Surface) -> None:
        screen.fill(self._tm.background_color or (0, 0, 0))

        for tile in self._background:
            screen.blit(tile.image, tile.rect)

        for x in sorted(self._sprites + [self._player] + self._foreground, key=lambda s: s.position[1]):
            screen.blit(x.image, x.rect)

        #for tile in self._foreground:
            #screen.blit(tile.image, tile.rect)

    def update(self, frame_delta: int) -> None:

        if self.game_input.is_triggered(kb.INVENTORY):
            for x in self._sprites:
                x.execute("toggle")

        if self.game_input.is_triggered(key=pygame.K_q):
            self._player.execute(actions.TOGGLE_BOUNDING_BOX)
            for x in self._sprites:
                x.execute(actions.TOGGLE_BOUNDING_BOX)

        if self.game_input.is_triggered(kb.MOVE_UP):
            self._player.execute(actions.START_MOVING, directions.UP)
        if self.game_input.is_released(kb.MOVE_UP):
            self._player.execute(actions.STOP_MOVING, directions.UP)

        if self.game_input.is_triggered(kb.MOVE_DOWN):
            self._player.execute(actions.START_MOVING, directions.DOWN)
        if self.game_input.is_released(kb.MOVE_DOWN):
            self._player.execute(actions.STOP_MOVING, directions.DOWN)

        if self.game_input.is_triggered(kb.MOVE_LEFT):
            self._player.execute(actions.START_MOVING, directions.LEFT)
        if self.game_input.is_released(kb.MOVE_LEFT):
            self._player.execute(actions.STOP_MOVING, directions.LEFT)

        if self.game_input.is_triggered(kb.MOVE_RIGHT):
            self._player.execute(actions.START_MOVING, directions.RIGHT)
        if self.game_input.is_released(kb.MOVE_RIGHT):
            self._player.execute(actions.STOP_MOVING, directions.RIGHT)

        for x in self._sprites + [self._player]:
            x.update(frame_delta)
