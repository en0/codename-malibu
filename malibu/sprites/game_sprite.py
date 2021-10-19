from typing import Set, Dict

from .null_components import NullGraphicsComponent, NullPhysicsComponent, NullInputComponent
from ..enum import ComponentMessageEnum
from ..mixins import LoggerMixin
from ..typing import (
    IGameSprite,
    INotifierGameSprite,
    IGameSpriteInputComponent,
    IGameSpritePhysicsComponent,
    IGameSpriteGraphicsComponent,
    INotifiableComponent,
)


class GameSprite(LoggerMixin, IGameSprite, INotifierGameSprite):

    @property
    def input_component(self) -> IGameSpriteInputComponent:
        return self._input_component

    @input_component.setter
    def input_component(self, val: IGameSpriteInputComponent) -> None:
        self.log.info("Registering Component %s->%s", self.__class__.__name__, val.__class__.__name__)
        self._input_component = val
        val.set_container(self)

    @property
    def physics_component(self) -> IGameSpritePhysicsComponent:
        return self._physics_component

    @physics_component.setter
    def physics_component(self, val: IGameSpritePhysicsComponent) -> None:
        self.log.info("Registering Component %s->%s", self.__class__.__name__, val.__class__.__name__)
        self._physics_component = val
        val.set_container(self)

    @property
    def graphics_component(self) -> IGameSpriteGraphicsComponent:
        return self._graphics_component

    @graphics_component.setter
    def graphics_component(self, val: IGameSpriteGraphicsComponent) -> None:
        self.log.info("Registering Component %s->%s", self.__class__.__name__, val.__class__.__name__)
        self._graphics_component = val
        val.set_container(self)

    def subscribe(self, msg_type: ComponentMessageEnum, component: INotifiableComponent):
        self._subscribed.setdefault(msg_type, set()).add(component)

    def broadcast(self, sender: object, msg_type: ComponentMessageEnum, value: any):
        for component in self._subscribed.get(msg_type):
            if component is not sender:
                component.notify(sender, msg_type, value)

    def __init__(self):
        self._subscribed: Dict[ComponentMessageEnum, Set[INotifiableComponent]] = dict()
        self._input_component: IGameSpriteInputComponent = NullInputComponent()
        self._physics_component: IGameSpritePhysicsComponent = NullPhysicsComponent()
        self._graphics_component: IGameSpriteGraphicsComponent = NullGraphicsComponent()

