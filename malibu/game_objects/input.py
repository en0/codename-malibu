import pygame
from collections import deque

from ..services import ServiceLocator
from ..enum import GameObjectMessageEnum, StateEnum
from ..typing import IBehaviorComponent, IWorldMap, IGameObject


class SimpleKBInputComponent(IBehaviorComponent):
    parent: IGameObject

    def set_parent(self, game_object: IGameObject):
        self.parent = game_object

    def update(self, frame_delta: float, world: IWorldMap):
        keyboard = ServiceLocator.get_keyboard()

        if keyboard.is_pressed(pygame.K_w):
            self.md.appendleft("UP")
        if keyboard.is_pressed(pygame.K_s):
            self.md.appendleft("DOWN")
        if keyboard.is_pressed(pygame.K_a):
            self.md.appendleft("LEFT")
        if keyboard.is_pressed(pygame.K_d):
            self.md.appendleft("RIGHT")

        if keyboard.is_released(pygame.K_w):
            self.md.remove("UP")
        if keyboard.is_released(pygame.K_s):
            self.md.remove("DOWN")
        if keyboard.is_released(pygame.K_a):
            self.md.remove("LEFT")
        if keyboard.is_released(pygame.K_d):
            self.md.remove("RIGHT")

        # TODO: Input component has no business setting a velocity. Likely, it should
        # simply broadcast or set a facing direction and toggle a moving flag.
        if len(self.md):
            if self.md[0] == "UP":
                self.set_velocity(pygame.Vector2(0, -1))
            elif self.md[0] == "DOWN":
                self.set_velocity(pygame.Vector2(0, 1))
            elif self.md[0] == "LEFT":
                self.set_velocity(pygame.Vector2(-1, 0))
            elif self.md[0] == "RIGHT":
                self.set_velocity(pygame.Vector2(1, 0))
        else:
            self.set_velocity(pygame.Vector2(0, 0))


    def set_velocity(self, vector: pygame.Vector2):
        self.parent.set_state(StateEnum.TARGET_VECTOR, vector)

    def __init__(self):
        self.md = deque()

