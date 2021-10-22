import pygame
from typing import List, Tuple
from .sandbox import SceneSandbox
from ..services import ServiceLocator
from ..enum import AudioEdgeTransitionEnum, GameObjectEnum, SceneEnum
from ..typing import IGameObject, IGameScene, IWorldMap


class PlayScene(SceneSandbox, IGameScene):

    _map_surface: pygame.Surface
    _objects: List[IGameObject] = []
    _player: IGameObject
    _map: IWorldMap = None

    @property
    def player_location(self) -> pygame.Vector2:
        return pygame.Vector2(0)

    def activate(self) -> None:
        self._player = self.create_object(GameObjectEnum.HERO)
        self._objects.append(self._player)
        self._map = self.load_world("demo")
        self.play_music(self._map.get_default_music())
        self._map_surface = pygame.Surface(self._map.get_rect().size)
        self._camera = self.create_camera(self._map.get_rect())
        self._camera.attach_to(self._player)

    def inactivate(self) -> None:
        pass

    def process_inputs(self) -> None:
        for obj in self._objects:
            obj.process_input(self.keyboard)
        if self.keyboard.is_pressed(pygame.K_ESCAPE):
            self.push_to_scene(SceneEnum.GAME_MENU)

    def update(self, frame_delta: float) -> None:
        for obj in self._objects:
            obj.update(frame_delta, self._map)
        self._map.update(frame_delta)

    def render(self) -> None:
        self._map_surface.fill((0, 0, 0))
        self._map.render(self._map_surface, self._camera.aperture)
        for obj in self._objects:
            obj.render(self._map_surface)
        self.graphics.blit(self._map_surface, self._camera.world_offset)
