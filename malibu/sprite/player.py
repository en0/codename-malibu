import pygame

from malibu_lib import BasicAnimation
from malibu_lib.typing import IAssetManager
from malibu_lib.abc import GameSprite


class PlayerSprite(GameSprite):

    @property
    def image(self) -> pygame.Surface:
        return self.anim.image

    def update(self, frame_delta: int) -> None:
        self.anim.update(frame_delta)

    def __init__(self, am: IAssetManager):
        self.spec = am.get_sprite_spec("base-boi")
        self.anim = BasicAnimation(self.spec.animations["run-right"], am)
