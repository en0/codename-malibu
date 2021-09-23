from abc import ABC, abstractmethod
from pygame import Surface
from pygame.event import Event
from typing import List, Tuple, Optional

from .model import SpriteSpec, GameSettings


class IGameScene(ABC):
    """A Game Scene"""

    @abstractmethod
    def render(self, screen: Surface):
        """Render the current scene to the given display"""
        ...

    @abstractmethod
    def reconfigure(self, settings: GameSettings):
        """Initialize/Reinitialize the scene based on the given settings."""
        ...

    @abstractmethod
    def process_event(self, event: Event):
        """An optional method to process pygame events"""
        ...

    @abstractmethod
    def update(self, frame_delta: int):
        """Update the current game state"""
        ...

    @abstractmethod
    def startup(self):
        """Initialize the current scene"""
        ...

    @abstractmethod
    def shutdown(self):
        """Shutdown and cleanup the scene"""
        ...


class IGame(ABC):
    """A Game context"""

    @abstractmethod
    def set_scene(self, next_scene: IGameScene):
        """Set the current scene"""
        ...

    @abstractmethod
    def play(self):
        """Begin playing the game"""
        ...

    @abstractmethod
    def reconfigure(self, settings: GameSettings):
        """Initialize/Reinitialize the game based on the given settings."""
        ...

    @abstractmethod
    def close(self):
        """Stop playing the game"""
        ...


class IAssetManager(ABC):
    """Manages the loading of assets"""

    @property
    @abstractmethod
    def module(self) -> str:
        """Get the module used by the asset manager"""
        ...

    @abstractmethod
    def get_sprite_spec_path(self, sprite_name: str) -> str:
        """Get the full path for a sprite spec"""
        ...

    @abstractmethod
    def get_sprite_sheet_path(self, sheet_name: str) -> str:
        """Get the full path for a sprite sheet"""
        ...

    @abstractmethod
    def list_sprite_specs(self) -> List[SpriteSpec]:
        """List all sprite Secifications"""
        ...

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

    @property
    @abstractmethod
    def current_frame_index(self):
        """Get the current frame index."""
        ...

    @abstractmethod
    def has_flag(self, flag_name: str) -> bool:
        """Check if the animation has the given flag."""
        ...

    @abstractmethod
    def update(self, frame_delta: int) -> None:
        """Update the animation"""
        ...

    @abstractmethod
    def reset(self) -> None:
        """Reset the animation frames."""
        ...


class IGameInput(ABC):
    """Track game input"""

    @abstractmethod
    def reconfigure(self, settings: GameSettings) -> None:
        """Configure/Reconfigure inputs"""
        ...

    @abstractmethod
    def is_pressed(self, mapped: Optional[str] = None, key: Optional[int] = None, button: Optional[int] = None) -> bool:
        """Check if a key is currently pressed (held down)"""
        ...

    @abstractmethod
    def is_triggered(self, mapped: Optional[str] = None, key: Optional[int] = None, button: Optional[int] = None) -> bool:
        """Check if a key was just pressed."""
        ...

    @abstractmethod
    def get_mouse_pos(self) -> Tuple[int, int]:
        """Get the current mouse x, y position"""
        ...

    @abstractmethod
    def process_event(self, event: Event) -> None:
        """Process pygame events."""
        ...

    @abstractmethod
    def update(self, frame_delta: int):
        """Reset the trigger keys collection

        This should be called after game objects have collected input states
        """
        ...
