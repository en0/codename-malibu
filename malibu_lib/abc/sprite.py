from ..typing import IGameSprite, IAssetManager
from ..mixin import EventListenerMixin


class GameSprite(EventListenerMixin, IGameSprite):
    ...
