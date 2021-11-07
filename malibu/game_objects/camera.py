from ..typing import IGameObject, IWorldMap, IBehaviorComponent
from ..mixins import GraphicMixin, AudioMixin


class CameraComponent(GraphicMixin, AudioMixin, IBehaviorComponent):
    parent: IGameObject

    def set_parent(self, game_object: IGameObject):
        self.parent = game_object

    def update(self, frame_delta: float, world: IWorldMap):
        self.graphics.set_focus(self.parent.data.location)
        self.audio.set_focus(self.parent.data.location)
