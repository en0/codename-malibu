from pygame import Surface, draw
import pygame

from malibu_lib.model import GameSettings
from malibu_lib.typing import IGameScene, IGameInput


class MainMenuScene(IGameScene):

    def reconfigure(self, settings: GameSettings) -> None:
        pass

    def render(self, screen: Surface) -> None:
        draw.circle(screen, (0, 255, 0), self.x, 3)

    def update(self, frame_delta: int) -> None:
        m = 1 * (frame_delta / 10.0)
        x, y = self.x
        if self.game_input.is_pressed(key=pygame.K_w):
            y -= m
        if self.game_input.is_pressed(key=pygame.K_s):
            y += m
        if self.game_input.is_pressed(key=pygame.K_a):
            x -= m
        if self.game_input.is_pressed(key=pygame.K_d):
            x += m
        self.x = (x, y)

    def startup(self) -> None:
        pass

    def shutdown(self) -> None:
        pass

    def process_event(self, event) -> None:
        pass

    def __init__(self, game_input: IGameInput):
        self.game_input = game_input
        self.x = (0, 0)
