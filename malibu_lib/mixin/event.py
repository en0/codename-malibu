from pygame import USEREVENT, QUIT
from pygame.event import Event, post

from ..utils import publish_game_event, is_game_event

USER_TYPE = "GAME_TOPIC"


class EventListenerMixin:
    """Add event processor loop that dispatches events to on_* methods."""

    def process_event(self, event: Event) -> None:
        if event.type == QUIT and hasattr(self, "on_quit"):
            fn = getattr(self, "on_quit")
            fn(event)
        elif is_game_event(event):
            method = f"on_{event.topic.lower()}"
            if hasattr(self, method):
                fn = getattr(self, method)
                fn(event)


class EventPublisherMixin:
    """Add publish method that dispatches events."""

    def publish(self, topic: str, **data):
        publish_game_event(topic, **data)
