import pygame

from .component_base import ComponentBase
from ..services import ServiceLocator
from ..typing import IInputComponent, IWorldMap, IKeyboardService
from ..enum import GameObjectMessageEnum


class KBInput(ComponentBase, IInputComponent):

    normal_input_map = {
        GameObjectMessageEnum.MOVE_UP: pygame.K_w,
        GameObjectMessageEnum.MOVE_DOWN: pygame.K_s,
        GameObjectMessageEnum.MOVE_LEFT: pygame.K_a,
        GameObjectMessageEnum.MOVE_RIGHT: pygame.K_d,
    }

    # Other things this needs to do:
    #  move (up, down, left, right)
    #  toggle-run
    #  attack
    #  interact
    #  toggle-inventory

    @property
    def keyboard(self) -> IKeyboardService:
        return ServiceLocator.get_keyboard()

    def update(self, frame_delta: float, world: IWorldMap) -> None:
        for msg_type, key in self._active_map.items():
            if self.keyboard.is_pressed(key):
                self.notify(msg_type, True)
            if self.keyboard.is_released(key):
                self.notify(msg_type, False)

    def __init__(self):
        self._active_map = self.normal_input_map
