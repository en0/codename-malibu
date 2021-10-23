from pygame import Surface

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


class NullPhysicsComponent(IPhysicsComponent):
    def set_parent(self, game_object: IGameObject): ...
    def update(self, frame_delta: float, world: IWorldMap): ...


class NullGraphicsComponent(IGraphicsComponent):
    def set_parent(self, game_object: IGameObject): ...
    def render(self, gfx: Surface): ...
