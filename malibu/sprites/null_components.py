from pygame import Surface

from ..typing import (
    IGameSpriteInputComponent,
    INotifierGameSprite,
    IKeyboardService,
    IGameSpritePhysicsComponent,
    IGameSpriteGraphicsComponent,
)


class NullInputComponent(IGameSpriteInputComponent):
    def set_container(self, sprite: INotifierGameSprite): ...
    def process_input(self, keyboard: IKeyboardService): ...


class NullPhysicsComponent(IGameSpritePhysicsComponent):
    def update(self): ...
    def set_container(self, sprite: INotifierGameSprite): ...


class NullGraphicsComponent(IGameSpriteGraphicsComponent):
    def render(self, gfx: Surface): ...
    def set_container(self, sprite: INotifierGameSprite): ...
