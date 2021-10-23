import pygame
from typing import List, Optional, Type, Dict
from .enum import ComponentMessageEnum
from .components import (
    NullInputComponent,
    NullPhysicsComponent,
    NullGraphicsComponent,
)
from .typing import (
    IGameObject,
    IGameComponent,
    IGraphicsComponent,
    IInputComponent,
    IKeyboardService,
    INotifiableObject,
    IPhysicsComponent,
    IWorldMap,
    T_GameComponent,
)


class GameObject(IGameObject):

    def process_input(self, keyboard: IKeyboardService):
        self._input.process_input(keyboard)

    def update(self, frame_delta: float, world: IWorldMap):
        self._phys.update(frame_delta, world)

    def render(self, gfx: pygame.Surface):
        self._gfx.render(gfx)

    def receive_message(self, sender: object, msg_type: ComponentMessageEnum, value: any):
        for component in self._subscriptions.get(msg_type, []):
            if component is not sender:
                component.receive_message(sender, msg_type, value)

    def subscribe(self, msg_type: ComponentMessageEnum, component: INotifiableObject):
        self._subscriptions.setdefault(msg_type, []).append(component)

    def unsubscribe(self, msg_type: ComponentMessageEnum, component: INotifiableObject):
        try:
            self._subscriptions.get(msg_type, []).remove(component)
        except ValueError:
            pass

    def get_component(self, component_type: Type[T_GameComponent]) -> Optional[T_GameComponent]:
        for component in self._components:
            if isinstance(component, component_type):
                return component
        return None

    def __init__(self, components: List[IGameComponent]) -> None:
        self._components = components.copy()
        self._subscriptions: Dict[ComponentMessageEnum, List[INotifiableObject]] = dict()
        self._input = self.get_component(IInputComponent) or NullInputComponent()
        self._phys = self.get_component(IPhysicsComponent) or NullPhysicsComponent()
        self._gfx = self.get_component(IGraphicsComponent) or NullGraphicsComponent()
        for component in components:
            component.set_parent(self)
