from pygame import Surface
from logging import getLogger, Logger

from ..typing import (
    IAudioService,
    IKeyboardService,
    IAssetService,
    ISettingsService,
    IGameService,
    ISceneFactory,
    IObjectFactory,
    IWorldFactory,
    ICameraFactory,
)


class ServiceLocator:

    _game: IGameService = None
    _camera_factory: ICameraFactory
    _scene_factory: ISceneFactory = None
    _object_factory: IObjectFactory = None
    _graphics: Surface = None
    _audio: IAudioService = None
    _keyboard: IKeyboardService = None
    _asset_manager: IAssetService = None
    _settings_manager: ISettingsService = None
    _world_factory: IWorldFactory = None

    @classmethod
    def get_camera_factory(cls) -> ICameraFactory:
        return cls._camera_factory

    @classmethod
    def get_world_factory(cls) -> IWorldFactory:
        return cls._world_factory

    @classmethod
    def get_scene_factory(cls) -> ISceneFactory:
        return cls._scene_factory

    @classmethod
    def get_object_factory(cls) -> IObjectFactory:
        return cls._object_factory

    @classmethod
    def get_game(cls) -> IGameService:
        return cls._game

    @classmethod
    def get_settings(cls) -> ISettingsService:
        return cls._settings_manager

    @classmethod
    def get_graphics(cls) -> Surface:
        return cls._graphics

    @classmethod
    def get_audio(cls) -> IAudioService:
        return cls._audio

    @classmethod
    def get_keyboard(cls) -> IKeyboardService:
        return cls._keyboard

    @classmethod
    def get_asset_manager(cls) -> IAssetService:
        return cls._asset_manager

    @classmethod
    def set_camera_factory_provider(cls, camera_factory: ICameraFactory) -> None:
        cls._camera_factory = camera_factory

    @classmethod
    def set_world_factory_provider(cls, world_factory: IWorldFactory) -> None:
        cls._world_factory = world_factory

    @classmethod
    def set_scene_factory_provider(cls, scene_factory: ISceneFactory) -> None:
        cls._scene_factory = scene_factory

    @classmethod
    def set_object_factory_provider(cls, object_factory: IObjectFactory) -> None:
        cls._object_factory = object_factory

    @classmethod
    def set_game_provider(cls, game: IGameService):
        cls._game = game

    @classmethod
    def set_settings_provider(cls, settings_manager: ISettingsService):
        cls._settings_manager = settings_manager

    @classmethod
    def set_audio_provider(cls, audio: IAudioService):
        cls._audio = audio

    @classmethod
    def set_graphics_provider(cls, graphics: Surface):
        cls._graphics = graphics

    @classmethod
    def set_keyboard_provider(cls, keyboard: IKeyboardService):
        cls._keyboard = keyboard

    @classmethod
    def set_asset_provider(cls, asset_manager: IAssetService):
        cls._asset_manager = asset_manager

    @classmethod
    def get_logger(cls, module: str) -> Logger:
        return getLogger(module)

    @classmethod
    def install_default_providers(cls):

        from .asset_manager import AssetManager
        asset_manager = AssetManager()
        cls.set_asset_provider(asset_manager)

        from .settings_manager import SettingsManager
        settings_manager = SettingsManager()
        cls.set_settings_provider(settings_manager)

        from .keyboard import KeyboardService
        keyboard_provider = KeyboardService()
        cls.set_keyboard_provider(keyboard_provider)

        from .audio import AudioService
        audio_provider = AudioService()
        cls.set_audio_provider(audio_provider)

        from .game import GameService
        game_provider = GameService()
        cls.set_game_provider(game_provider)

        from pygame import display, FULLSCREEN, HWACCEL, DOUBLEBUF
        from ..const import SCREEN_SIZE
        graphics_provider = display.set_mode(SCREEN_SIZE, HWACCEL | DOUBLEBUF)
        cls.set_graphics_provider(graphics_provider)

        from .scene_factory import SceneFactory
        scene_factory = SceneFactory()
        cls.set_scene_factory_provider(scene_factory)

        from .object_factory import ObjectFactory
        object_factory = ObjectFactory()
        cls.set_object_factory_provider(object_factory)

        from .world_factory import MapFactory
        world_factory = MapFactory()
        cls.set_world_factory_provider(world_factory)

        from .camera import CameraFactory
        camera_factory = CameraFactory()
        cls.set_camera_factory_provider(camera_factory)

        # Init
        from logging import basicConfig
        basicConfig(level="DEBUG")
        asset_manager.initialize()
        audio_provider.initialize()
