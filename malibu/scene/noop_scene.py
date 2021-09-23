from pygame import Surface

from malibu_lib.model import GameSettings
from malibu_lib.typing import IGameScene


class NoOpScene(IGameScene):

    def reconfigure(self, settings: GameSettings):
        pass

    def render(self, screen: Surface):
        pass

    def update(self, frame_delta: int):
        pass

    def startup(self):
        pass

    def shutdown(self):
        pass
