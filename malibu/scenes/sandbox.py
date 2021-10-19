from typing import Optional

from ..enum import AudioEdgeTransitionEnum, SceneEnum, SpriteEnum
from ..mixins import KeyboardMixin, LoggerMixin, GraphicMixin
from ..services import ServiceLocator


class SceneSandbox(KeyboardMixin, LoggerMixin, GraphicMixin):

    @classmethod
    def play_music(cls, name: str, edge: Optional[AudioEdgeTransitionEnum] = None) -> None:
        ServiceLocator.get_audio().set_music(name, edge)

    @classmethod
    def switch_to_scene(cls, name: SceneEnum):
        scene = ServiceLocator.get_scene_factory().new(name)
        ServiceLocator.get_game().set_scene(scene)

    @classmethod
    def create_sprite(cls, name: SpriteEnum):
        return ServiceLocator.get_sprite_factory().new(name)

    @classmethod
    def load_map(cls, name: str):
        return ServiceLocator.get_map_factory().get_tile_map(name)
