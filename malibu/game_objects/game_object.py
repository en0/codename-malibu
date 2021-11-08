import pygame
from typing import List, Optional, Type, Dict, Set
from .graphics import DefaultGraphicsComponent
from ..enum import GameObjectMessageEnum, StateEnum
from ..typing import (
    IGameObject,
    IGraphicsComponent,
    INotifiableObject,
    IWorldMap,
    IBehaviorComponent,
)


class GameObject(IGameObject):

    def get_state(self, key: StateEnum) -> Optional[any]:
        return self._data.get(key)

    def set_state(self, key: StateEnum, value: any) -> None:
        self._data[key] = value
        self.notify(self, GameObjectMessageEnum.STATE_CHANGED, key)

    def has_tag(self, tag: str) -> bool:
        return tag in self._tags

    def add_tag(self, tag: str) -> None:
        self._tags.add(tag)
        self.notify(self, GameObjectMessageEnum.ADD_TAG, tag)

    def remove_tag(self, tag: str) -> None:
        try:
            self._tags.remove(tag)
            self.notify(self, GameObjectMessageEnum.REMOVE_TAG, tag)
        except KeyError:
            pass

    def update(self, frame_delta: float, world: IWorldMap):
        for c in self._behaviors:
            c.update(frame_delta, world)

    def render(self, gfx: pygame.Surface):
        self._gfx.render(gfx)

    def notify(self, sender: object, msg_type: GameObjectMessageEnum, value: any):
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
    ) -> None:
        self._tags = set(tags)
        self._data: Dict[StateEnum, any] = {}
        self._behaviors = behaviors.copy()
        self._subscriptions: Dict[GameObjectMessageEnum, Set[INotifiableObject]] = dict()
        self._gfx = graphics or DefaultGraphicsComponent()
        self._gfx.set_parent(self)
        for behavior in self._behaviors:
            behavior.set_parent(self)
