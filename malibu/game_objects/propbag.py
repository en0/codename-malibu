from .base import GameComponentBase
from ..enum import GameObjectMessageEnum
from ..typing import IGameComponent


class PropertyComponent(IPropertyComponent, GameComponentBase):

    def receive_message(self, sender: object, msg_type: GameObjectMessageEnum, value: any):
        self.bag[msg_type] = value

    def set_parent(self, game_object: IGameObject):
        self.parent = game_object
        self.parent.subscribe(GameObjectMessageEnum.ALL)

    def get_property(self, msg_type: GameObjectMessageEnum, default: any = None) -> any:
        return self.bag.get(msgtype, default)

    def __init__(self):
        self.bag: Dict[GameObjectMessageEnum, any] = {}
        self.parent: IGameObject = None


