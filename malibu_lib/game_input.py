import pygame
from typing import Tuple, Optional, List, Union, Set

from .typing import IGameInput, ISettingManager
from .model import GameSettings


def _k(key: int) -> Tuple[str, int]:
    return "key", key


def _m(button: int) -> Tuple[str, int]:
    return "mouse", button


class GameInput(IGameInput):

    def process_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            self.pressed.add(_k(event.key))
            self.triggered.add(_k(event.key))
        elif event.type == pygame.KEYUP and _k(event.key) in self.pressed:
            self.pressed.remove(_k(event.key))
            self.released.add(_k(event.key))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.pressed.add(_m(event.button))
            self.triggered.add(_m(event.button))
        elif event.type == pygame.MOUSEBUTTONUP and _m(event.button) in self.pressed:
            self.pressed.remove(_m(event.button))
        elif event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos

    def update(self, frame_delta: int) -> None:
        self.triggered = set()
        self.released = set()

    def is_pressed(self, mapped: Optional[str] = None, key: Optional[int] = None, button: Optional[int] = None) -> bool:
        return (
            _k(key) in self.pressed if key is not None else
            _m(button) in self.pressed if button is not None else
            self.input_map.get(mapped) in self.pressed if mapped is not None else
            False
        )

    def is_released(self, mapped: Optional[str] = None, key: Optional[int] = None, button: Optional[int] = None) -> bool:
        return (
            _k(key) in self.released if key is not None else
            _m(button) in self.released if button is not None else
            self.input_map.get(mapped) in self.released if mapped is not None else
            False
        )

    def is_triggered(self, mapped: Optional[str] = None, key: Optional[int] = None, button: Optional[int] = None) -> bool:
        return (
            _k(key) in self.triggered if key is not None else
            _m(button) in self.triggered if button is not None else
            self.input_map.get(mapped) in self.triggered if mapped is not None else
            False
        )

    def get_mouse_pos(self) -> Tuple[int, int]:
        return self.mouse_pos

    def on_settings_changed(self, event: pygame.event.Event) -> None:
        self._reconfigure(event.settings)

    def _reconfigure(self, settings: GameSettings) -> None:
        input_settings = settings.input_settings.copy()
        self.input_map = {a: (t, k) for a, (t, k) in input_settings.items()}

    def __init__(self, settings_manager: ISettingManager) -> None:
        self.settings_manager = settings_manager
        self.mouse_pos: Tuple[int, int] = 0, 0
        self.pressed = set()
        self.triggered = set()
        self.released = set()
        self.input_map = dict()

        # Configure inputs
        settings = self.settings_manager.get_settings()
        self._reconfigure(settings)
