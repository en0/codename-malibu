from typing import Callable, Dict

from .locator import ServiceLocator
from ..enum import SceneEnum
from ..typing import ISceneFactory, IGameScene
from ..scenes import *


class SceneFactory(ISceneFactory):

    def new(self, scene: SceneEnum) -> IGameScene:
        return self._builders[scene]()

    def _overlay_game_menu(self) -> IGameScene:
        return GameMenu(ServiceLocator.get_game().get_current_scene())

    def __init__(self):
        self._builders: Dict[SceneEnum, Callable[[], IGameScene]] = {
            SceneEnum.SPLASH: SplashScene,
            #SceneEnum.MAIN_MENU: NullScene,
            SceneEnum.MAIN_MENU: PlayScene,
            SceneEnum.PLAY: PlayScene,
            SceneEnum.GAME_MENU: self._overlay_game_menu,
        }
