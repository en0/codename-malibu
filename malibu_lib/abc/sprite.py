from pygame import Surface, Rect, draw
from typing import Dict, Optional, List, Tuple

from ..typing import IGameSprite, IAssetManager, IGameItem
from ..model import SpriteSpec
from ..animation import BasicAnimation


class GameSprite(IGameSprite):
    """A game sprite based on sprite specification data."""

    sprite_name: str

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
        surf = self.animation.image.copy()
        if self._show_bounding_box:
            fp = self.animation.get_footprint()
            bb = self.animation.get_boundary()
            draw.rect(surf, (255,0,0), bb, width=1)
            draw.rect(surf, (0,0,255), fp, width=1)
        return surf

    @property
    def rect(self) -> Rect:
        rect = self.animation.image.get_rect()
        fp = self.animation.get_footprint()
        rect.midbottom = self._position
        rect.bottom += rect.height - fp.bottom
        rect.centerx += (rect.width/2) - fp.centerx
        return rect

    @property
    def position(self) -> Tuple[float, float]:
        return self._position

    @position.setter
    def position(self, value: Tuple[float, float]) -> None:
        self._position = value

    @property
    def inventory(self) -> Dict[str, IGameItem]:
        return self._inventory

    def update(self, frame_delta: int) -> None:
        self.animation.update(frame_delta)

    def execute(self, action: str, *args, **kwargs) -> None:
        meth = f"on_{action.lower()}"
        if hasattr(self, meth):
            fn = getattr(self, meth)
            fn(*args, **kwargs)

    def on_toggle_bounding_box(self):
        self._show_bounding_box = not self._show_bounding_box

    def __init__(self, am: IAssetManager):
        self._show_bounding_box = False
        self._animation_manager = am
        self._spec = am.get_sprite_spec(self.sprite_name)
        self._active_animation = self._spec.default_animation
        self._animations = {k: BasicAnimation(v, am) for k, v in self._spec.animations.items()}
        self._position = 0, 0
        self._inventory = {}
