from ..typing import IGameObject, IWorldMap, IBehaviorComponent
from ..mixins import GraphicMixin, AudioMixin
from ..enum import StateEnum


class CameraComponent(GraphicMixin, AudioMixin, IBehaviorComponent):
    parent: IGameObject

    def set_parent(self, game_object: IGameObject):
        self.parent = game_object

    def update(self, frame_delta: float, world: IWorldMap):
        self.graphics.set_focus(self.parent.get_state(StateEnum.WORLD_LOCATION))
        self.audio.set_focus(self.parent.get_state(StateEnum.WORLD_LOCATION))
