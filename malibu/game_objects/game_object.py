import pygame
from typing import List, Optional, Type, Dict, Set
from .null import (
    NullInputComponent,
    NullPhysicsComponent,
    NullGraphicsComponent,
)
from ..enum import GameObjectMessageEnum
from ..typing import (
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

    def has_tag(self, tag: str) -> bool:
        return tag in self._tags

    def process_input(self, keyboard: IKeyboardService):
        self._input.process_input(keyboard)

    def update(self, frame_delta: float, world: IWorldMap):
        self._phys.update(frame_delta, world)

    def render(self, gfx: pygame.Surface):
        self._gfx.render(gfx)

    def receive_message(self, sender: object, msg_type: GameObjectMessageEnum, value: any):
        for component in self._get_matching_subs(msg_type):
            if component is not sender:
                component.receive_message(sender, msg_type, value)

    def _get_matching_subs(self, msg_type: GameObjectMessageEnum) -> Set[INotifiableObject]:
        return (
            self._subscriptions.get(msg_type, set()) |
            self._subscriptions.get(GameObjectMessageEnum.ALL, set())
        )

    def subscribe(self, msg_type: GameObjectMessageEnum, component: INotifiableObject):
        self._subscriptions.setdefault(msg_type, set()).add(component)

    def unsubscribe(self, msg_type: GameObjectMessageEnum, component: INotifiableObject):
        try:
            self._subscriptions.get(msg_type, set()).remove(component)
        except ValueError:
            pass

    def get_component(self, component_type: Type[T_GameComponent]) -> Optional[T_GameComponent]:
        for component in self._components:
            if isinstance(component, component_type):
                return component
        return None

    def __init__(self, tags: List[str], components: List[IGameComponent]) -> None:
        self._tags = set(tags)
        self._components = components.copy()
        self._subscriptions: Dict[GameObjectMessageEnum, Set[INotifiableObject]] = dict()
        self._input = self.get_component(IInputComponent) or NullInputComponent()
        self._phys = self.get_component(IPhysicsComponent) or NullPhysicsComponent()
        self._gfx = self.get_component(IGraphicsComponent) or NullGraphicsComponent()
        for component in components:
            component.set_parent(self)
