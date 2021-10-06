from pygame import Surface, Rect
from typing import Dict, Optional, List, Tuple

from ..typing import IGameSprite, IAssetManager
from ..mixin import EventListenerMixin
from ..model import SpriteSpec
from ..animation import BasicAnimation


class GameSprite(EventListenerMixin, IGameSprite):
    """A game sprite based on sprite specification data."""

    sprite_name: str

    @property
    def position(self) -> Tuple[float, float]:
        return self._position

    @position.setter
    def position(self, value: Tuple[float, float]) -> None:
        self._position = value

    @property
    def asset_manager(self) -> IAssetManager:
        return self._animation_manager

    @property
    def sprite_spec(self) -> SpriteSpec:
        return self._spec

    @property
    def animation(self) -> BasicAnimation:
        return (
            self._animations[self._active_animation]
            if self._animations else None
        )

    @property
    def active_animation(self) -> str:
        return self._active_animation

    @active_animation.setter
    def active_animation(self, value: str):
        self._active_animation = value

    def list_animations(self) -> List:
        return (
            list(self._animations.keys())
            if self._animations else []
        )

    # IGameSprite Interface
    @property
    def image(self) -> Surface:
        return self.animation.image

    @property
    def rect(self) -> Rect:
        rect = self.animation.image.get_rect()
        rect.midleft = self._position
        return rect

    def update(self, frame_delta: int) -> None:
        self.animation.update(frame_delta)

    def __init__(self, am: IAssetManager):
        self._animation_manager = am
        self._spec = am.get_sprite_spec(self.sprite_name)
        self._active_animation = self._spec.default_animation
        self._animations = {k: BasicAnimation(v, am) for k, v in self._spec.animations.items()}
        self._position = 0, 0
