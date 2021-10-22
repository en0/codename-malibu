from pygame import Rect
from typing import Optional

from ..typing import ICamera
from ..enum import AudioEdgeTransitionEnum, SceneEnum, GameObjectEnum
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

    @classmethod
    def create_camera(cls, world: Rect) -> ICamera:
        return ServiceLocator().get_camera_factory().create_camera(world)
