from pygame import Vector2
from typing import List, Union, Dict
from importlib import import_module
from ..models import ObjectDataComponentSpec
from ..mixins import AssetMixin
from ..typing import IObjectFactory, IGameObject
from ..game_objects import *


components_module = import_module("...game_objects", package=__name__)


class ComponentFactory:

    @classmethod
    def new(cls, spec: ObjectDataComponentSpec):
        # TODO: Handle args and kwargs
        klass = getattr(components_module, spec.klass)
        return klass(*spec.args, **spec.kwargs)


class ObjectFactory(AssetMixin, IObjectFactory):

    _hero_instance = None

    def new(self, name: str) -> IGameObject:
        dat = self.asset_manager.get_object_data(name)
        gfx = self._component_factory.new(dat.graphics_component)
        ai = self._component_factory.new(dat.input_component)
        behavior = [self._component_factory.new(spec) for spec in dat.behavior_components]
        obj = GameObject(
            tags=dat.tags,
            input_component=ai,
            graphics_component=gfx,
            behavior_components=behavior)
        return obj

    def __init__(self):
        self._component_factory = ComponentFactory()
