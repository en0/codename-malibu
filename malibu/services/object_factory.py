from pygame import Vector2
from ..game_object import GameObject
from ..enum import GameObjectEnum, ComponentMessageEnum
from ..typing import IObjectFactory, IGameObject
from ..components import *


class ObjectFactory(IObjectFactory):

    _hero_instance = None

    def new(self, sprite_name: GameObjectEnum) -> IGameObject:
        return self._constructors[sprite_name]()

    def new_text_sprite(self, value: str, pos: Vector2) -> IGameObject:
        sprite = GameObject()
        #sprite.graphics_component = FontComponent()
        return sprite

    def get_hero(self):
        if self._hero_instance is None:
            self._hero_instance = GameObject([
                SimpleKBInputComponent(),
                BasicPhysicsComponent(),
                TestGraphicsComponent(),
            ])
        return self._hero_instance

    def __init__(self):
        self._constructors = {
            GameObjectEnum.HERO: self.get_hero,
        }
