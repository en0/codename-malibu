from abc import ABC, abstractmethod
from pygame import Surface
from typing import List

from .model import SpriteSpec


class IAssetManager(ABC):
    """Manages the loading of assets"""

    @abstractmethod
    def get_sprite_spec(self, name: str) -> SpriteSpec:
        """Load a sprite spec of the given name"""
        ...

    @abstractmethod
    def get_sprite_sheet(self, name: str) -> List[Surface]:
        """Load a sprite sheet of the given name"""
        ...

    @abstractmethod
    def get_sprite_sheet_tile(self, sheet_name: str, id: int) -> Surface:
        """Get a single sprite sheet tile"""
        ...

    @abstractmethod
    def clear(self) -> None:
        """Clear all loaded assets"""
        ...

class IAnimation(ABC):
    """Manages animation tiles"""

    @property
    @abstractmethod
    def name(self) -> str:
        """Gets the name of the animation"""
        ...

    @property
    @abstractmethod
    def complete(self) -> bool:
        """Gets a bool indicating if the animation is complete."""
        ...

    @property
    @abstractmethod
    def image(self) -> Surface:
        """Gets the current frame as a surface"""
        ...

    @abstractmethod
    def has_flag(self, flag_name: str) -> bool:
        """Check if the animation has the given flag."""
        ...

    @abstractmethod
    def update(self, frame_delta: float) -> None:
        """Update the animation"""
        ...

    @abstractmethod
    def reset(self) -> None:
        """Reset the animation frames."""
        ...

