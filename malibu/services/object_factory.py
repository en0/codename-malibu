from pygame import Vector2
from typing import List, Union, Dict
from importlib import import_module
from ..mixins import AssetMixin
from ..typing import IObjectFactory, IGameObject
from ..game_objects import *


components_module = import_module("...game_objects", package=__name__)


class ComponentFactory:

    @classmethod
    def new(cls, name: str, args: Union[List[any], Dict[str, any]]):
        kwargs = args if isinstance(args, dict) else {}
        args = args if isinstance(args, list) else []
        klass = getattr(components_module, name)
        return klass(*args, **kwargs)


class ObjectFactory(AssetMixin, IObjectFactory):

    _hero_instance = None

    def new(self, name: str) -> IGameObject:
        dat = self.asset_manager.get_object_data(name)
        components = [
            self._component_factory.new(n, args)
            for n, args in dat.components.items()
        ]
        return GameObject(dat.tags, components, DefaultGraphicsComponent())

    def __init__(self):
        self._component_factory = ComponentFactory()
