import pygame

from .sandbox import SceneSandbox
from ..services import ServiceLocator
from ..enum import SceneEnum, AudioEdgeTransitionEnum



class SplashScene(SceneSandbox):

    @property
    def player_location(self) -> pygame.Vector2:
        return pygame.Vector2(0)

    def activate(self) -> None:
        self.audio.set_music("world2", AudioEdgeTransitionEnum.NONE)

    def inactivate(self) -> None:
        pass

    def process_inputs(self) -> None:
        if self.keyboard.is_pressed(pygame.K_RETURN):
            self.switch_to_scene(SceneEnum.MAIN_MENU)

    def update(self, frame_delta: float) -> None:
        pass

    def render(self) -> None:
        pass
