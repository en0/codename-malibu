import pygame
from typing import List, Tuple
from .sandbox import SceneSandbox
from ..enum import AudioEdgeTransitionEnum, SpriteEnum, SceneEnum
from ..typing import IGameObject, IGameScene, ITileMap
from ..lib import Camera


class PlayScene(SceneSandbox, IGameScene):

    _camera: Camera
    _map_surface: pygame.Surface
    _sprites: List[IGameObject] = []
    _player: IGameObject
    _map: ITileMap = None

    @property
    def player_location(self) -> pygame.Vector2:
        return self._player.position

    def activate(self) -> None:
        self._player = self.create_sprite(SpriteEnum.HERO)
        self._sprites.append(self._player)
        self._map = self.load_map("demo")
        self.play_music(self._map.get_default_music())
        self._map_surface = pygame.Surface(self._map.get_rect().size)
        self._camera = Camera(self.graphics.get_rect(), self._map.get_rect())

    def inactivate(self) -> None:
        pass

    def process_inputs(self) -> None:
        for sprite in self._sprites:
            sprite.input_component.process_input(self.keyboard)
        if self.keyboard.is_pressed(pygame.K_ESCAPE):
            self.push_to_scene(SceneEnum.GAME_MENU)

    def update(self, frame_delta: float) -> None:
        for sprite in self._sprites:
            sprite.physics_component.update(frame_delta, self._map)
        self._map.update(frame_delta)
        self._camera.set_focus(self.player_location)

    def render(self) -> None:
        self._map_surface.fill((0, 0, 0))
        self._map.render(self._map_surface, self._camera.aperture)
        for sprite in self._sprites:
            sprite.graphics_component.render(self._map_surface)
        self.graphics.blit(self._map_surface, self._camera.world_offset)
