import pygame
from collections import deque
from typing import Dict

from .commands import MoveCommand, NullCommand
from ..component_base import ComponentBase

from ...lib import OrderedSet
from ...services import ServiceLocator
from ...typing import IWorldMap, IControllerSource, IControllerCommand, IControllerComponent
from ...enum import DirectionEnum


class BufferedKeyboardController(ComponentBase, IControllerComponent, IControllerSource):

    def update(self, frame_delta: float, world: IWorldMap) -> None:
        for key, command in self._commands.items():
            if self._kb.is_pressed(key):
                self._buffer.add(key)
            if self._kb.is_released(key) and key in self._buffer:
                self._buffer.remove(key)

    def get_input(self) -> IControllerCommand:
        if self._buffer:
            return self._commands.get(self._buffer[-1])
        return self._null

    def __init__(self):
        self._kb = ServiceLocator.get_keyboard()
        self._queue = deque()
        self._buffer = OrderedSet()
        self._null = NullCommand()
        self._commands: Dict[int, IControllerCommand] = {
            pygame.K_w: MoveCommand(DirectionEnum.NORTH),
            pygame.K_s: MoveCommand(DirectionEnum.SOUTH),
            pygame.K_a: MoveCommand(DirectionEnum.WEST),
            pygame.K_d: MoveCommand(DirectionEnum.EAST),
        }
