from typing import List, Any, Optional

from ..typing import IGameObject
from ..enum import GameObjectMessageEnum, StateEnum
from ..mixins import NotifiableMixin


class ComponentBase(NotifiableMixin):

    subscriptions: List[GameObjectMessageEnum] = []
    _parent: IGameObject = None

    @property
    def parent(self) -> IGameObject:
        if self._parent is not None:
            return self._parent
        raise Exception("Parent not set!")

    def get_state(self, key: StateEnum) -> Optional[Any]:
        return self.parent.get_state(key)

    def set_state(self, key: StateEnum, value: Any) -> None:
        self.parent.set_state(key, value)

    def notify(self, msg_type: GameObjectMessageEnum, value: any):
        self._parent.notify(self, msg_type, value)

    def set_parent(self, game_object: IGameObject) -> None:
        self._parent = game_object
        if self.subscriptions:
            self.subscribe(game_object, self.subscriptions)
