from abc import ABC, abstractmethod
from typing import List

from pygame import Surface

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
