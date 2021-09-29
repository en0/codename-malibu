from pygame.event import Event, post
from pygame import USEREVENT

SETTINGS_CHANGED = "SETTINGS_CHANGED"
GAME_EVENT_TYPE = "GAME_TOPIC"


def is_game_event(event: Event) -> bool:
    return event.type == USEREVENT and event.user_type == GAME_EVENT_TYPE


def publish_game_event(topic: str, **data):
    post(Event(USEREVENT, user_type=GAME_EVENT_TYPE, topic=topic, **data))
