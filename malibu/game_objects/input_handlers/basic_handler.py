from ..component_base import ComponentBase
from ...enum import DirectionEnum
from ...typing import (
    IAnimationHandler,
    IBehaviorComponent,
    IControllerSource,
    IInputHandler,
    IPhysicsHandler,
    IWorldMap,
)


WALK_ANIMATIONS = {
    DirectionEnum.NORTH: "WALK_NORTH",
    DirectionEnum.SOUTH: "WALK_SOUTH",
    DirectionEnum.WEST: "WALK_WEST",
    DirectionEnum.EAST: "WALK_EAST",
}

IDLE_ANIMATIONS = {
    DirectionEnum.NORTH: "IDLE_NORTH",
    DirectionEnum.SOUTH: "IDLE_SOUTH",
    DirectionEnum.WEST: "IDLE_WEST",
    DirectionEnum.EAST: "IDLE_EAST",
}


class BasicInputHandler(ComponentBase, IBehaviorComponent, IInputHandler):

    _velocity = 0
    _heading = DirectionEnum.SOUTH
    _animation = IDLE_ANIMATIONS[DirectionEnum.SOUTH]
    _physics: IPhysicsHandler
    _controller: IControllerSource
    _animator: IAnimationHandler

    def move(self, direction: DirectionEnum) -> None:
        self._velocity = 100
        self._heading = direction
        self._animation = WALK_ANIMATIONS[direction]

    def update(self, frame_delta: float, world: IWorldMap) -> None:
        self._velocity = 0
        self._animation = IDLE_ANIMATIONS[self._heading]
        self._controller.get_input().execute(self)
        self._physics.set_vector(self._heading, self._velocity)
        self._animator.set_animation(self._animation)

    def startup(self, world: IWorldMap):
        self._controller = self.get_component(IControllerSource)
        self._animator = self.get_component(IAnimationHandler)
        self._physics = self.get_component(IPhysicsHandler)
