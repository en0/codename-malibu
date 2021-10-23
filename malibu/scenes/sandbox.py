from pygame import Rect
from typing import Optional

from ..enum import SceneEnum, GameObjectEnum
from ..mixins import KeyboardMixin, LoggerMixin, GraphicMixin, AudioMixin
from ..services import ServiceLocator


class SceneSandbox(KeyboardMixin, LoggerMixin, GraphicMixin, AudioMixin):

    @classmethod
    def switch_to_scene(cls, name: SceneEnum):
        scene = ServiceLocator.get_scene_factory().new(name)
        ServiceLocator.get_game().set_scene(scene)

    @classmethod
    def push_to_scene(cls, name: SceneEnum):
        scene = ServiceLocator.get_scene_factory().new(name)
        ServiceLocator.get_game().push_scene(scene)

    @classmethod
    def pop_to_scene(cls):
        ServiceLocator.get_game().pop_scene()

    @classmethod
    def create_object(cls, name: GameObjectEnum):
        return ServiceLocator.get_object_factory().new(name)

    @classmethod
    def load_world(cls, name: str):
        return ServiceLocator.get_world_factory().build_world(name)
