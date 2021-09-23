import pygame
from .typing import IEventBroadcaster


class PygameEventBroadcaster(IEventBroadcaster):

    def publish(self, topic, **data):
        event = pygame.event.Event(pygame.USEREVENT, topic=topic, **data)
        pygame.event.post(event)
