from ..mixin import EventListenerMixin, EventPublisherMixin
from ..typing import (
    IGameScene,
    IGameInput,
    ISettingManager,
    IAssetManager,
    IGameSceneFactory,
    IGameSpriteFactory,
    IGameSprite,
)


class SceneABC(EventListenerMixin, EventPublisherMixin, IGameScene):

    @property
    def game_input(self) -> IGameInput:
        return self._game_input

    @property
    def settings_manager(self) -> ISettingManager:
        return self._settings_manager

    @property
    def asset_manager(self) -> IAssetManager:
        return self._asset_manager

    def create_scene(self, name: str) -> IGameScene:
        return self._create_scene(name)

    def create_sprite(self, name: str, **kwargs) -> IGameSprite:
        sprite = self._create_sprite(name)
        sprite.initialize(**kwargs)
        return sprite

    def __init__(
        self,
        game_input: IGameInput,
        settings_manager: ISettingManager,
        asset_manager: IAssetManager,
        scene_factory: IGameSceneFactory,
        sprite_factory: IGameSpriteFactory,
    ) -> None:
        self._game_input = game_input
        self._settings_manager = settings_manager
        self._asset_manager = asset_manager
        self._create_scene = scene_factory
        self._create_sprite = sprite_factory
