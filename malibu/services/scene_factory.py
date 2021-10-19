from typing import Callable, Dict

from ..enum import SceneEnum
from ..typing import ISceneFactoryService, IGameScene
from ..scenes import *


class SceneFactoryService(ISceneFactoryService):

    def new(self, scene: SceneEnum) -> IGameScene:
        return self._builders[scene]()

    def __init__(self):
        self._builders: Dict[SceneEnum, Callable[[], IGameScene]] = {
            SceneEnum.SPLASH: SplashScene,
            #SceneEnum.MAIN_MENU: NullScene,
            SceneEnum.MAIN_MENU: PlayScene,
            SceneEnum.PLAY: PlayScene,
        }
