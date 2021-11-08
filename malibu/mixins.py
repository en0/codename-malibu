from typing import List, Dict, Callable
from logging import Logger
from .enum import GameObjectMessageEnum
from .services.locator import ServiceLocator
from .typing import (
    IAssetService,
    IAudioService,
    IGameObject,
    IGameService,
    IGraphicsService,
    IKeyboardService,
    INotifiableObject,
    IObjectFactory,
)

_SubMap_T = Dict[GameObjectMessageEnum, Callable[[object, any], None]]


class AssetMixin:
    @property
    def asset_manager(self) -> IAssetService:
        return ServiceLocator.get_asset_manager()


class LoggerMixin:
    @property
    def log(self) -> Logger:
        return ServiceLocator.get_logger(self.__class__.__name__)


class KeyboardMixin:
    @property
    def keyboard(self) -> IKeyboardService:
        return ServiceLocator.get_keyboard()


class AudioMixin:
    @property
    def audio(self) -> IAudioService:
        return ServiceLocator.get_audio()


class GraphicMixin:
    @property
    def graphics(self) -> IGraphicsService:
        return ServiceLocator.get_graphics()


class GameMixin:
    @property
    def game(self) -> IGameService:
        return ServiceLocator.get_game()


class SceneFactoryMixin:
    @property
    def scene_factory(self):
        return ServiceLocator.get_scene_factory()


class ObjectFactoryMixin:
    @property
    def object_factory(self) -> IObjectFactory:
        return ServiceLocator.get_object_factory()


class NotifiableMixin(INotifiableObject):

    _sub_map: _SubMap_T = None

    def receive_message(self, sender: object, msg_type: GameObjectMessageEnum, value: any):
        self._sub_map[msg_type](sender, value)

    def subscribe(self, container: IGameObject, subs: List[GameObjectMessageEnum]):
        self._sub_map = {}
        for sub in subs:
            container.subscribe(sub, self)
            fn_name = f"on_{sub.name.lower()}"
            self._sub_map[sub] = getattr(self, fn_name)
