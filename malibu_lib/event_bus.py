import pygame

from .typing import IEventBus
from .events import *


class PygameUserEventBus(IEventBus):

    def publish(self, topic, **data) -> None:
        event = pygame.event.Event(pygame.USEREVENT, user_type="GAME_TOPIC", topic=topic, **data)
        pygame.event.post(event)

    def attach(self, topic, callback) -> None:
        self._subs[topic] = callback

    def process_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.USEREVENT:
            return
        if event.user_type != "GAME_TOPIC":
            return
        if event.topic in self._subs:
            self._subs[event.topic](event)

    def __init__(self):
        self._subs = {}
