from abc import ABC, abstractmethod
from pygame import Surface
from pygame.event import Event
from typing import List, Tuple, Optional, Callable

from .model import SpriteSpec, GameSettings


EventCallback = Callable[[Event], None]


class IGameScene(ABC):
    """A Game Scene"""

    @abstractmethod
    def process_event(self, event: Event) -> None:
        """Process pygame events."""
        ...

    @abstractmethod
    def update(self, frame_delta: int) -> None:
        """Update the current game state"""
        ...

    @abstractmethod
    def render(self, screen: Surface) -> None:
        """Render the current scene to the given display"""
        ...

    @abstractmethod
    def startup(self) -> None:
        """Initialize the current scene"""
        ...

    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown and cleanup the scene"""
        ...


class IGame(ABC):
    """A Game context"""

    @abstractmethod
    def startup(self) -> None:
        """Called when the game starts."""
        ...

    @abstractmethod
    def shutdown(self) -> None:
        """Called right before the game closes."""
        ...

    @abstractmethod
    def set_scene(self, next_scene: str) -> None:
        """Set the current scene"""
        ...

    @abstractmethod
    def play(self) -> None:
        """Begin playing the game"""
        ...

    @abstractmethod
    def close(self) -> None:
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
    def current_frame_index(self) -> None:
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
    def update(self, frame_delta: int) -> None:
        """Reset the trigger keys collection

        This should be called after game objects have collected input states
        """
        ...


class ISettingManager(ABC):
    """Manage Game Settings"""

    @abstractmethod
    def get_settings(self) -> GameSettings:
        """Fetch the game settings"""
        ...

    @abstractmethod
    def set_settings(self, settings: GameSettings) -> None:
        """Replace game settings with new ones."""
        ...


class IPathProvider(ABC):
    """Provides the appropriate paths considering the operating system"""

    @abstractmethod
    def get_log_path(self, file: str, version: str=None) -> str:
        """Get a file inside the log directory"""
        ...

    @abstractmethod
    def get_config_path(self, file: str, version: str=None) -> str:
        """Get a file inside the config directory"""
        ...

    @abstractmethod
    def get_data_path(self, file: str, version: str=None) -> str:
        """Get a file inside the data directory"""
        ...

    @abstractmethod
    def ensure_log_dir_exists(self, version: str=None) -> None:
        """Create the log directory if it doesn't exist."""
        ...

    @abstractmethod
    def ensure_config_dir_exists(self, version: str=None) -> None:
        """Create the config directory if it doesn't exist."""
        ...

    @abstractmethod
    def ensure_data_dir_exists(self, version: str=None) -> None:
        """Create the data directory if it doesn't exist."""
        ...


class IGameSprite(ABC):

    @property
    @abstractmethod
    def image(self) -> Surface:
        """The image to render"""
        ...

    @abstractmethod
    def process_event(self, event: Event) -> None:
        """Process pygame events."""
        ...

    @abstractmethod
    def update(self, frame_delta: int) -> None:
        """Update the current sprite."""
        ...


IGameSceneFactory = Callable[[str], IGameScene]
IGameSpriteFactory = Callable[[str], IGameSprite]

