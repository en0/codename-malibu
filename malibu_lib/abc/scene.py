from ..typing import IGameScene, IGameInput
from ..mixin import EventListenerMixin


class SceneABC(IGameScene, EventListenerMixin):

    @property
    def game_input(self) -> IGameInput:
        return self._game_input

    def startup(self) -> None:
        ...

    def shutdown(self) -> None:
        ...

    def __init__(self, game_input: IGameInput):
        self._game_input = game_input
