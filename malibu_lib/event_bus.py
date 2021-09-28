import pygame

from .typing import IEventBus
from .events import *


class PygameUserEventBus(IEventBus):

    def publish(self, topic, **data) -> None:
        event = pygame.event.Event(pygame.USEREVENT, user_type="GAME_TOPIC", topic=topic, **data)
        pygame.event.post(event)

    def attach(self, topic, callback) -> None:
        self._subs.setdefault(topic, set()).add(callback)

    def detach(self, callback) -> None:
        for callbacks in self._subs.values():
            if callback in callbacks:
                callbacks.remove(callback)

    def process_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT and GAME_EXIT in self._subs:
            exit_event = pygame.event.Event(
                pygame.USEREVENT,
                user_type="GAME_TOPIC",
                topic=GAME_EXIT)
            for cb in self._subs[GAME_EXIT]:
                cb(exit_event)

        if (event.type == pygame.USEREVENT and
            event.user_type == "GAME_TOPIC" and
            event.topic in self._subs
        ):
            for cb in self._subs.get(event.topic, []):
                cb(event)

    def __init__(self):
        self._subs = {}
        self._raw_subs = {}
