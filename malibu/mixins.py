from pygame import Surface
from logging import Logger
from .services.locator import ServiceLocator
from .typing import (
    IAssetService,
    IKeyboardService,
    IAudioService,
    IObjectFactory,
    IGameService,
    IGraphicsService,
)


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
