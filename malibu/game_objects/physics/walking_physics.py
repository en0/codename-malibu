from pygame import Rect
from typing import Tuple

from ..component_base import ComponentBase
from ...enum import StateEnum, DirectionEnum
from ...typing import IPhysicsHandler, IWorldMap, IBehaviorComponent


class WalkingPhysics(ComponentBase, IBehaviorComponent, IPhysicsHandler):

    _heading: DirectionEnum
    _velocity: float

    def set_vector(self, heading: DirectionEnum, velocity: float):
        self._heading = heading
        self._velocity = velocity

    def get_vector(self) -> Tuple[DirectionEnum, float]:
        return self._heading, self._velocity

    def update(self, frame_delta: float, world: IWorldMap) -> None:
        if not (self._velocity and self._heading):
            return

        vx, vy = self._get_vector()
        footprint: Rect = self.get_state(StateEnum.FOOTPRINT).copy()
        cx, cy = self.get_state(StateEnum.WORLD_LOCATION)
        nx = (vx * frame_delta) + cx
        ny = (vy * frame_delta) + cy
        footprint.center = nx, ny

        if world.is_walkable(footprint):
            self.set_state(StateEnum.WORLD_LOCATION, (nx, ny))

    def _get_vector(self):
        return {
            DirectionEnum.NORTH: (0, -self._velocity),
            DirectionEnum.SOUTH: (0, self._velocity),
            DirectionEnum.WEST: (-self._velocity, 0),
            DirectionEnum.EAST: (self._velocity, 0),
        }[self._heading]
