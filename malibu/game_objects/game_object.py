import pygame
from typing import List, Optional, Type, Dict, Set
from .spatial import SpatialComponent
from .null import (
    NullInputComponent,
    NullPhysicsComponent,
    NullGraphicsComponent,
)
from ..enum import GameObjectMessageEnum
from ..typing import (
    IGameComponent,
    IGameObject,
    IGraphicsComponent,
    IInputComponent,
    IKeyboardService,
    INotifiableObject,
    IPhysicsComponent,
    ISpatialComponent,
    IWorldMap,
    T_GameComponent,
)


class GameObject(IGameObject):

    def has_tag(self, tag: str) -> bool:
        return tag in self._tags

    def add_tag(self, tag: str) -> None:
        self._tags.add(tag)

    def remove_tag(self, tag: str) -> None:
        try:
            self._tags.remove(tag)
        except KeyError:
            pass

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
        self._input = self.get_component(IInputComponent)
        self._phys = self.get_component(IPhysicsComponent)
        self._gfx = self.get_component(IGraphicsComponent)

        if self._input is None:
            self._input = NullInputComponent()
            self._components.append(self._input)

        if self._phys is None:
            self._phys = NullPhysicsComponent()
            self._components.append(self._phys)

        if self._gfx is None:
            self._gfx = NullGraphicsComponent()
            self._components.append(self._gfx)

        if self.get_component(ISpatialComponent) is None:
            self._components.append(SpatialComponent())

        for component in self._components:
            component.set_parent(self)
