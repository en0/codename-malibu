from .component_base import ComponentBase
from ..typing import IWorldMap, IBehaviorComponent
from ..mixins import GraphicMixin, AudioMixin
from ..enum import StateEnum


class AttachedCamera(ComponentBase, GraphicMixin, AudioMixin, IBehaviorComponent):

    def update(self, frame_delta: float, world: IWorldMap):
        self.graphics.set_focus(self.get_state(StateEnum.WORLD_LOCATION))
        self.audio.set_focus(self.get_state(StateEnum.WORLD_LOCATION))
