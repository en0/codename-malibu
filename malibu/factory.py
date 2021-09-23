"""Handle the creation of all game objects."""

from pyioc3 import StaticContainerBuilder, Container, ScopeEnum
from typing import Callable, Optional
from malibu_lib.typing import (
    IGame,
    IGameInput,
    IGameScene,
)


_ioc: Optional[Container] = None


def _next_generator():
    i = 0
    while True:
        i += 1
        yield i


_ng = _next_generator()
auto = lambda: next(_ng)


SCENE_SPLASH = auto()
SCENE_MAIN_MENU = auto()
SCENE_SETTINGS_MENU = auto()


def _build_ioc() -> Container:

    ioc = StaticContainerBuilder()

    # Game Clock

    from pygame.time import Clock
    ioc.bind(Clock, Clock)

    # Bind the main game object

    from .game import MalibuGame

    def activate_game(g: IGame):

        g.set_scene(get_scene(SCENE_MAIN_MENU))

        import pygame
        from malibu_lib.model import GameSettings, VideoSettings
        # TODO: This should get the settings manager
        g.reconfigure(GameSettings(
            video_settings=VideoSettings(),
            input_settings={
                "attack": ("key", pygame.K_SPACE),
                "inventory": ("mouse", pygame.BUTTON_LEFT),
            }
        ))
        return g

    ioc.bind(
        annotation=IGame,
        implementation=MalibuGame,
        scope=ScopeEnum.SINGLETON,
        on_activate=activate_game)

    # Bind the Game Input

    from malibu_lib import GameInput

    ioc.bind(
        annotation=IGameInput,
        implementation=GameInput,
        scope=ScopeEnum.SINGLETON)

    # Game Scenes

    from .scene import MenuScene
    ioc.bind(SCENE_MAIN_MENU, MenuScene)

    return ioc.build()


def _get_ioc() -> Container:
    global _ioc
    if _ioc is None:
        _ioc = _build_ioc()
    return _ioc


def _get(interface, annotation=None):
    try:
        ret = _get_ioc().get(annotation or interface)
    except KeyError as ex:
        raise ValueError("The given type does not exist") from ax
    if not isinstance(ret, interface):
        raise ValueError("The given type does not exist")
    return ret


def get_game() -> IGame:
    return _get(IGame)


def get_scene(scene: int) -> IGameScene:
    return _get(IGameScene, scene)

