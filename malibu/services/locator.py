from pygame import Surface
from logging import getLogger, Logger

from ..typing import (
    IAudioService,
    IKeyboardService,
    IAssetService,
    ISettingsService,
    IGameService,
    ISceneFactoryService,
    ISpriteFactoryService,
    IMapFactoryService,
)


class ServiceLocator:

    _game: IGameService = None
    _scene_factory: ISceneFactoryService = None
    _sprite_factory: ISpriteFactoryService = None
    _graphics: Surface = None
    _audio: IAudioService = None
    _keyboard: IKeyboardService = None
    _asset_manager: IAssetService = None
    _settings_manager: ISettingsService = None
    _map_factory: IMapFactoryService = None

    @classmethod
    def get_map_factory(cls) -> IMapFactoryService:
        return cls._map_factory

    @classmethod
    def get_scene_factory(cls) -> ISceneFactoryService:
        return cls._scene_factory

    @classmethod
    def get_sprite_factory(cls) -> ISpriteFactoryService:
        return cls._sprite_factory

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
    def set_map_factory_provider(cls, map_factory: IMapFactoryService) -> None:
        cls._map_factory = map_factory

    @classmethod
    def set_scene_factory_provider(cls, scene_factory: ISceneFactoryService) -> None:
        cls._scene_factory = scene_factory

    @classmethod
    def set_sprite_factory_provider(cls, sprite_factory: ISpriteFactoryService) -> None:
        cls._sprite_factory = sprite_factory

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
        graphics_provider = display.set_mode(SCREEN_SIZE, FULLSCREEN | HWACCEL | DOUBLEBUF)
        cls.set_graphics_provider(graphics_provider)

        from .scene_factory import SceneFactoryService
        scene_factory = SceneFactoryService()
        cls.set_scene_factory_provider(scene_factory)

        from .sprite_factory import SpriteFactoryService
        sprite_factory = SpriteFactoryService()
        cls.set_sprite_factory_provider(sprite_factory)

        from .map_factory import MapFactoryService
        map_factory = MapFactoryService()
        cls.set_map_factory_provider(map_factory)

        # Init
        from logging import basicConfig
        basicConfig(level="DEBUG")
        asset_manager.initialize()
        audio_provider.initialize()
