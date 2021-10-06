from malibu_lib.utils import counter

from .noop_scene import NullScene
from .main_menu import MainMenuScene

_auto = counter()
SCENE_SPLASH = f"SCENE_{_auto()}"
SCENE_MAIN_MENU = f"SCENE_{_auto()}"
SCENE_SETTINGS_MENU = f"SCENE_{_auto()}"

__all__ = [
    "SCENE_SPLASH",
    "SCENE_MAIN_MENU",
    "SCENE_SETTINGS_MENU",
]
