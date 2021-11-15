from ..component_base import ComponentBase
from ...typing import IBehaviorComponent, IWorldMap, IAnimationHandler


class Chest(ComponentBase, IBehaviorComponent):
    animator: IAnimationHandler

    def update(self, frame_delta: float, world: IWorldMap) -> None:
        pass

    def startup(self, world: IWorldMap) -> None:
        self.animator = self.get_component(IAnimationHandler)
        self.animator.set_animation("CLOSED")