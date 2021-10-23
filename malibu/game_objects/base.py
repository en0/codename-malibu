from abc import abstractmethod
from typing import List, Dict, Callable
from ..enum import GameObjectMessageEnum
from ..typing import IGameComponent, IGameObject

SubMap_T = Dict[GameObjectMessageEnum, Callable[[object, any], None]]

class GameComponentBase(IGameComponent):

    subscriptions: List[GameObjectMessageEnum] = []

    _sub_map: SubMap_T = None
    _parent: IGameObject = None

    @property
    def parent(self) -> IGameObject:
        return self._parent

    def receive_message(self, sender: object, msg_type: GameObjectMessageEnum, value: any):
        self._sub_map[msg_type](sender, value)

    def set_parent(self, game_object: IGameObject):
        self._sub_map = {}
        self._parent = game_object
        for sub in self.subscriptions:
            self._parent.subscribe(sub, self)
            self._sub_map[sub] = getattr(self, sub.name.lower())
