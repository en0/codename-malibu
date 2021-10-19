import pygame
from pygame.event import Event
from typing import Set, Iterable

from ..typing import IKeyboardService


class KeyboardService(IKeyboardService):

    def is_pressed(self, key: int) -> bool:
        return key in self._pressed

    def is_released(self, key: int) -> bool:
        return key in self._released

    def is_held(self, key: int) -> bool:
        return key in self._held

    def get_pressed(self) -> Set[int]:
        return self._pressed.copy()

    def get_released(self) -> Set[int]:
        return self._released.copy()

    def get_held(self) -> Set[int]:
        return self._held.copy()

    def update(self, events: Iterable[Event]) -> None:
        self._pressed = set()
        self._released = set()
        for event in events:
            if event.type == pygame.KEYDOWN:
                self._pressed.add(event.key)
                self._held.add(event.key)
            elif event.type == pygame.KEYUP:
                self._released.add(event.key)
                if event.key in self._held:
                    self._held.remove(event.key)

    def __init__(self) -> None:
        self._held = set()
        self._pressed = set()
        self._released = set()
