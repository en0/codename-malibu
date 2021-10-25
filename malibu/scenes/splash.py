import pygame

from .sandbox import SceneSandbox
from ..services import ServiceLocator
from ..enum import SceneEnum, AudioEdgeTransitionEnum



class SplashScene(SceneSandbox):

    def activate(self) -> None:
        self.audio.set_music(None, AudioEdgeTransitionEnum.NONE)

    def inactivate(self) -> None:
        pass

    def update(self, frame_delta: float) -> None:
        if self.keyboard.is_pressed(pygame.K_RETURN):
            self.switch_to_scene(SceneEnum.MAIN_MENU)
