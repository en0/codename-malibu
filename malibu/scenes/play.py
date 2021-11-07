import pygame
from typing import List
from .sandbox import SceneSandbox
from ..enum import SceneEnum
from ..typing import IGameObject, IGameScene, IWorldMap


class PlayScene(SceneSandbox, IGameScene):

    objects: List[IGameObject] = []
    world: IWorldMap = None

    def activate(self) -> None:
        self.world = self.load_world("demo")
        self.audio.set_music(self.world.get_default_music())
        self.graphics.set_world_boundary(self.world.get_rect())

    def inactivate(self) -> None:
        pass

    def update(self, frame_delta: float) -> None:
        if self.keyboard.is_pressed(pygame.K_ESCAPE):
            self.push_to_scene(SceneEnum.GAME_MENU)
        self.world.update(frame_delta)
        self.graphics.fill((0, 0, 0))
        self.world.render(self.graphics)
