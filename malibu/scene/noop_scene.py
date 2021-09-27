from pygame import Surface

from malibu_lib.model import GameSettings
from malibu_lib.typing import IGameScene


class NullScene(IGameScene):

    def reconfigure(self, settings: GameSettings) -> None:
        pass

    def render(self, screen: Surface) -> None:
        pass

    def update(self, frame_delta: int) -> None:
        pass

    def startup(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def process_event(self, event) -> None:
        pass
