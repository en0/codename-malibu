from pygame import Vector2, Rect
from .component_base import ComponentBase
from ..enum import StateEnum, DirectionEnum
from ..typing import IBehaviorComponent


class WalkingPhysics(ComponentBase, IBehaviorComponent):

    @property
    def velocity(self):
        return self.get_state(StateEnum.VELOCITY)

    @property
    def heading(self):
        return self.get_state(StateEnum.HEADING)

    def _get_vector(self):
        return {
            DirectionEnum.NORTH: (0, -self.velocity),
            DirectionEnum.SOUTH: (0, self.velocity),
            DirectionEnum.WEST: (-self.velocity, 0),
            DirectionEnum.EAST: (self.velocity, 0),
        }[self.heading]

    def update(self, frame_delta: float, world: "IWorldMap") -> None:
        if not (self.velocity and self.heading):
            return

        vx, vy = self._get_vector()
        footprint: Rect = self.get_state(StateEnum.FOOTPRINT).copy()
        cx, cy = self.get_state(StateEnum.WORLD_LOCATION)
        nx = (vx * frame_delta) + cx
        ny = (vy * frame_delta) + cy
        footprint.center = nx, ny

        if world.is_walkable(footprint):
            self.set_state(StateEnum.WORLD_LOCATION, (nx, ny))
