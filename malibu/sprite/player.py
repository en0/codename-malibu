from typing import Dict
from malibu_lib.abc import GameSprite

from . import directions

class PlayerSprite(GameSprite):

    sprite_name = "base-boi"
    _move_speed: float = 0.05

    # Using dict as a ordered set - Python3+
    _moving: Dict[str, None]

    def on_start_moving(self, d):
        self._moving[d] = None

    def on_stop_moving(self, d):
        if d in self._moving:
            del self._moving[d]

    def update(self, frame_delta: int) -> None:
        if self._moving:
            *_, direct = self._moving.keys()
            x, y = self.position
            if direct == directions.UP:
                y = y - (self._move_speed * frame_delta)
                self.active_animation = "run-up"
            elif direct == directions.DOWN:
                y = y + (self._move_speed * frame_delta)
                self.active_animation = "run-down"
            elif direct == directions.LEFT:
                x = x - (self._move_speed * frame_delta)
                self.active_animation = "run-left"
            elif direct == directions.RIGHT:
                x = x + (self._move_speed * frame_delta)
                self.active_animation = "run-right"
            self.position = x, y
        elif not self._moving:
            self.active_animation = "breath"

        super().update(frame_delta)

    def initialize(self, **kwargs) -> None:
        self._moving = {}
        self.position = kwargs.get("position", (0, 0))
