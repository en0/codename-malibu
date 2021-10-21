from pygame import Vector2
from ..enum import SpriteEnum, ComponentMessageEnum
from ..typing import ISpriteFactoryService, IGameObject
from ..sprites import *


class SpriteFactoryService(ISpriteFactoryService):

    _hero_instance = None

    def new(self, sprite_name: SpriteEnum) -> IGameObject:
        return self._constructors[sprite_name]()

    def new_text_sprite(self, value: str, pos: Vector2) -> IGameObject:
        sprite = GameObject()
        #sprite.graphics_component = FontComponent()
        return sprite

    def get_hero(self):
        from ..sprites.testing import TestInputComponent, TestPhysicsComponent, TestGraphicsComponent
        if self._hero_instance is None:
            self._hero_instance = GameObject()
            self._hero_instance.input_component = TestInputComponent()
            self._hero_instance.physics_component = TestPhysicsComponent()
            self._hero_instance.graphics_component = TestGraphicsComponent()
        return self._hero_instance

    def __init__(self):
        self._constructors = {
            SpriteEnum.HERO: self.get_hero,
        }
