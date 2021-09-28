from abc import abstractmethod

from ..utils import auto_wireup_events
from ..typing import IGameScene, IEventBus, IGameInput


class SceneABC(IGameScene):

    @property
    def game_input(self) -> IGameInput:
        return self._game_input

    @property
    def ebus(self) -> IEventBus:
        return self._ebus

    def load(self) -> None:
        """Load the current scene"""
        ...

    def unload(self) -> None:
        """Unload the current scene"""
        ...

    def process_event(self, event) -> None:
        """An optional method to process pygame events"""
        ...

    def startup(self) -> None:
        self.load()
        self.cbs = auto_wireup_events(self._ebus, self)

    def shutdown(self) -> None:
        for cbs in self._cbs or []:
            self._ebus.detach(cbs)
        self.unload()

    def __init__(self, ebus: IEventBus, game_input: IGameInput):
        self._ebus = ebus
        self._game_input = game_input
        self._cbs = None
