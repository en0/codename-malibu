from malibu_lib.utils import counter

from .player import PlayerSprite
from .campfire import CampfireSprite
from .chest import ChestSprite
from .map_tile import MapTileSprite

_auto = counter()
SPRITE_PLAYER = f"SPRITE_{_auto()}"
SPRITE_CAMPFIRE = f"SPRITE_{_auto()}"
SPRITE_CHEST = f"SPRITE_{_auto()}"
SPRITE_MAP_TILE = f"SPRITE_{_auto()}"

__all__ = [
    "SPRITE_PLAYER",
    "SPRITE_CAMPFIRE",
    "SPRITE_CHEST",
    "SPRITE_MAP_TILE",
]
