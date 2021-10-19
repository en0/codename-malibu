import pygame
from typing import List
from pytmx import load_pygame, TiledTileLayer
from .sandbox import SceneSandbox
from ..enum import AudioEdgeTransitionEnum, SpriteEnum
from ..typing import IGameSprite, IGameScene, ITileMap


class PlayScene(SceneSandbox, IGameScene):

    _sprites: List[IGameSprite] = []
    _player: IGameSprite
    _map: ITileMap = None
    _all_tiles = {}

    @property
    def player_location(self) -> pygame.Vector2:
        # TODO: This is not the right solution
        return self._player.physics_component._pos

    def activate(self) -> None:

        self._player = self.create_sprite(SpriteEnum.HERO)
        self._sprites.append(self._player)
        self._map = self.load_map("demo")
        self.play_music(self._map.get_default_music())

    def inactivate(self) -> None:
        pass

    def process_inputs(self) -> None:
        for sprite in self._sprites:
            sprite.input_component.process_input(self.keyboard)

    def update(self, frame_delta: float) -> None:
        for sprite in self._sprites:
            sprite.physics_component.update(frame_delta, self._map)
        self._map.update(frame_delta)

    def render(self) -> None:
        self.graphics.fill((0, 0, 0))
        self._map.render(self.graphics)
        for sprite in self._sprites:
            sprite.graphics_component.render(self.graphics)
