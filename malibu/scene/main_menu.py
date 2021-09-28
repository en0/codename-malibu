from pygame import Surface, draw
import pygame

from malibu_lib.abc import SceneABC
from malibu_lib.model import GameSettings
from malibu_lib.typing import IGameInput


class MainMenuScene(SceneABC):

    x = (0, 0)

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
        if self.game_input.is_triggered(key=pygame.K_8):
            self.ebus.publish("SOME_TRIGGER")

        self.x = (x, y)

    def on_some_trigger(self, event):
        print("HIT", event)
