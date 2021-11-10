import pygame

from .component_base import ComponentBase

from ..typing import IBehaviorComponent, IWorldMap
from ..enum import GameObjectMessageEnum, DirectionEnum, StateEnum


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


class BufferedMovement(ComponentBase, IBehaviorComponent):

    subscriptions = [
        GameObjectMessageEnum.MOVE_UP,
        GameObjectMessageEnum.MOVE_DOWN,
        GameObjectMessageEnum.MOVE_LEFT,
        GameObjectMessageEnum.MOVE_RIGHT,
    ]

    def on_move_up(self, sender: object, value: bool):
        self._buffer_move(DirectionEnum.NORTH, value)

    def on_move_down(self, sender: object, value: bool):
        self._buffer_move(DirectionEnum.SOUTH, value)

    def on_move_left(self, sender: object, value: bool):
        self._buffer_move(DirectionEnum.WEST, value)

    def on_move_right(self, sender: object, value: bool):
        self._buffer_move(DirectionEnum.EAST, value)

    def update(self, frame_delta: float, world: IWorldMap) -> None:
        if self._buffer:
            facing = self._buffer[-1]
            self.set_state(StateEnum.HEADING, facing)
            self.set_state(StateEnum.VELOCITY, self._velocity)
            self.notify(GameObjectMessageEnum.SET_ANIMATION, WALK_ANIMATIONS[facing])
        else:
            facing = self.get_state(StateEnum.HEADING) or DirectionEnum.SOUTH
            self.set_state(StateEnum.VELOCITY, 0)
            self.notify(GameObjectMessageEnum.SET_ANIMATION, IDLE_ANIMATIONS[facing])

    def _buffer_move(self, direction: DirectionEnum, state: bool):
        if state:
            self._buffer.append(direction)
        else:
            self._buffer.remove(direction)

    def __init__(self):
        self._buffer = list()
        self._velocity = 100
