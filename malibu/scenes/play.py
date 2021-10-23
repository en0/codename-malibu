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
    world: IWorldMap = None

    @property
    def player_location(self) -> pygame.Vector2:
        return pygame.Vector2(0)

    def activate(self) -> None:
        self._player = self.create_object(GameObjectEnum.HERO)
        self._objects.append(self._player)
        self.world = self.load_world("demo")
        self.audio.set_music(self.world.get_default_music())
        self._map_surface = pygame.Surface(self.world.get_rect().size)
        self.camera.set_world_rect(self.world.get_rect())
        self.camera.attach(self._player)
        self.audio.attach(self._player)

    def inactivate(self) -> None:
        self.camera.detach(self._player)
        self.audio.detach(self._player)

    def process_inputs(self) -> None:
        for obj in self._objects:
            obj.process_input(self.keyboard)
        if self.keyboard.is_pressed(pygame.K_ESCAPE):
            self.push_to_scene(SceneEnum.GAME_MENU)

    def update(self, frame_delta: float) -> None:
        for obj in self._objects:
            obj.update(frame_delta, self.world)
        self.world.update(frame_delta)

    def render(self) -> None:
        self._map_surface.fill((0, 0, 0))
        self.world.render(self._map_surface, self.camera.aperture)
        for obj in self._objects:
            obj.render(self._map_surface)
        self.graphics.blit(self._map_surface, self.camera.world_offset)
