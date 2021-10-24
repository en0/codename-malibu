from pygame import Vector2
from typing import List, Union, Dict
from importlib import import_module
from ..mixins import AssetMixin
from ..enum import GameObjectMessageEnum
from ..typing import IObjectFactory, IGameObject
from ..game_objects import *


components_module = import_module("...game_objects", package=__name__)


class ComponentFactory:

    def new(self, name: str, args: Union[List[any], Dict[str, any]]):
        kwargs = args if isinstance(args, dict) else {}
        args = args if isinstance(args, list) else []
        Klass = getattr(components_module, name)
        return Klass(*args, **kwargs)


class ObjectFactory(AssetMixin, IObjectFactory):

    _hero_instance = None

    def new(self, name: str) -> IGameObject:
        dat = self.asset_manager.get_object_data(name)
        print(dat)
        return GameObject(dat.tags, [
            self._component_factory.new(n, args)
            for n, args in dat.components.items()
        ])

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
        self._component_factory = ComponentFactory()
        self._constructors = {
            "hero": self.get_hero,
        }
