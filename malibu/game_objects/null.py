from math import inf
from pygame import Surface, Vector2, Rect
from typing import Union, Tuple

from ..enum import GameObjectMessageEnum
from ..typing import (
    IGameObject,
    IGraphicsComponent,
    IInputComponent,
    IKeyboardService,
    IPhysicsComponent,
    IWorldMap,
)


class NullInputComponent(IInputComponent):
    def set_parent(self, game_object: IGameObject): ...
    def process_input(self, keyboard: IKeyboardService): ...
    def receive_message(self, sender: object, msg_type: GameObjectMessageEnum, value: any): ...


class NullPhysicsComponent(IPhysicsComponent):
    def set_parent(self, game_object: IGameObject): ...
    def update(self, frame_delta: float, world: IWorldMap): ...
    def receive_message(self, sender: object, msg_type: GameObjectMessageEnum, value: any): ...
    def get_location(self) -> Vector2: Vector2(0)


class NullGraphicsComponent(IGraphicsComponent):
    def set_parent(self, game_object: IGameObject): ...
    def render(self, gfx: Surface): ...
    def receive_message(self, sender: object, msg_type: GameObjectMessageEnum, value: any): ...
