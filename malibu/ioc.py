"""Handle the creation of all game objects."""

from pyioc3 import Container, ScopeEnum
from typing import Optional
from malibu_lib import ContainerBuilder
from malibu_lib.typing import IGame, IGameScene

from .config import game_config
from .game import MalibuGame

from .scene import *
from .scene import (
    MainMenuScene
)


_ioc: Optional[Container] = None


def _build_ioc() -> Container:

    ioc = ContainerBuilder()
    ioc.bind_defaults(game_config)

    ioc.bind(
        annotation=IGame,
        implementation=MalibuGame,
        scope=ScopeEnum.SINGLETON)

    ioc.bind(SCENE_MAIN_MENU, MainMenuScene)

    return ioc.build()


def get_game() -> IGame:
    global _ioc
    if _ioc is None:
        _ioc = _build_ioc()
    return _ioc.get(IGame)

