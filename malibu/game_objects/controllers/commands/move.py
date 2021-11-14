from ....typing import IControllerCommand, IInputHandler
from ....enum import DirectionEnum


class MoveCommand(IControllerCommand):

    def execute(self, actor: IInputHandler) -> None:
        actor.move(self._dir)

    def __init__(self, direction: DirectionEnum):
        self._dir = direction
