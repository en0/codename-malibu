import pygame
from typing import List, Optional, Type, Dict, Set
from .data import DataComponent
from .graphics import DefaultGraphicsComponent
from ..enum import GameObjectMessageEnum
from ..typing import (
    IGameObject,
    IGraphicsComponent,
    INotifiableObject,
    IDataComponent,
    IWorldMap,
    IBehaviorComponent,
)


class GameObject(IGameObject):

    @property
    def data(self) -> IDataComponent:
        return self._data

    def has_tag(self, tag: str) -> bool:
        return tag in self._tags

    def add_tag(self, tag: str) -> None:
        self._tags.add(tag)

    def remove_tag(self, tag: str) -> None:
        try:
            self._tags.remove(tag)
        except KeyError:
            pass

    def update(self, frame_delta: float, world: IWorldMap):
        for c in self._behaviors:
            c.update(frame_delta, world)

    def render(self, gfx: pygame.Surface):
        self._gfx.render(gfx)

    def receive_message(self, sender: object, msg_type: GameObjectMessageEnum, value: any):
        for component in self._get_matching_subs(msg_type):
            if component is not sender:
                component.receive_message(sender, msg_type, value)

    def subscribe(self, msg_type: GameObjectMessageEnum, component: INotifiableObject):
        self._subscriptions.setdefault(msg_type, set()).add(component)

    def unsubscribe(self, msg_type: GameObjectMessageEnum, component: INotifiableObject):
        try:
            self._subscriptions.get(msg_type, set()).remove(component)
        except ValueError:
            pass

    def _get_matching_subs(self, msg_type: GameObjectMessageEnum) -> Set[INotifiableObject]:
        return (
                self._subscriptions.get(msg_type, set()) |
                self._subscriptions.get(GameObjectMessageEnum.ALL, set())
        )

    def __init__(
        self,
        tags: List[str],
        behaviors: List[IBehaviorComponent],
        graphics: IGraphicsComponent = None,
        dat: IDataComponent = None,
    ) -> None:
        self._tags = set(tags)
        self._data = dat or DataComponent()
        self._behaviors = behaviors.copy()
        self._subscriptions: Dict[GameObjectMessageEnum, Set[INotifiableObject]] = dict()
        self._gfx = graphics or DefaultGraphicsComponent()
        self._gfx.set_parent(self)
        for behavior in self._behaviors:
            behavior.set_parent(self)
