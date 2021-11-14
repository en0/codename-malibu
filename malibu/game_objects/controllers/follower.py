from pygame import Vector2
from math import sqrt
from .commands import MoveCommand, NullCommand
from ..component_base import ComponentBase
from ...typing import IControllerSource, IWorldMap, IControllerCommand, IControllerComponent
from ...enum import StateEnum, DirectionEnum


class FollowerController(ComponentBase, IControllerComponent, IControllerSource):

    _player = None
    _command = None

    _null = NullCommand()
    _north = MoveCommand(DirectionEnum.NORTH)
    _south = MoveCommand(DirectionEnum.SOUTH)
    _west = MoveCommand(DirectionEnum.WEST)
    _east = MoveCommand(DirectionEnum.EAST)

    def get_input(self) -> IControllerCommand:
        return self._command or self._null

    def startup(self, world: IWorldMap):
        self._player = world.find_first_game_objects(lambda o: o.has_tag("player"))

    def update(self, frame_delta: float, world: IWorldMap) -> None:

        p = self._player
        target = Vector2(p.get_state(StateEnum.WORLD_LOCATION))
        current = Vector2(self.get_state(StateEnum.WORLD_LOCATION))
        delta = target - current
        dist = sqrt((delta.x ** 2) + (delta.y ** 2))

        if dist < 100:
            self._command = self._null

        elif abs(delta.x) > abs(delta.y):
            if delta.x < 0:
                self._command = self._west
            else:
                self._command = self._east

        else:
            if delta.y < 0:
                self._command = self._north
            else:
                self._command = self._south
