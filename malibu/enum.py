from enum import Enum, auto


class DirectionEnum(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4


class GameObjectMessageEnum(Enum):
    ALL = auto()
    STATE_CHANGED = auto()
    ADD_TAG = auto()
    REMOVE_TAG = auto()


class StateEnum(Enum):
    WORLD_LOCATION = auto()
    SPRITE_LOCATION = auto()
    SPRITE = auto()
    BOUNDING_BOX = auto()
    FOOTPRINT = auto()
    TARGET_VECTOR = auto()
    UPON_MATERIAL = auto()

class SceneEnum(Enum):
    SPLASH = auto()
    MAIN_MENU = auto()
    GAME_MENU = auto()
    SETTINGS = auto()
    PLAY = auto()


class AudioTypeEnum(Enum):
    MUSIC = 0
    KINETIC = 1
    PASSIVE = 2


class AudioEdgeTransitionEnum(Enum):
    NONE = 0
    CROSSFADE = 1
    FADEOUT = 2
    FADEIN = 3


class AudioCategoryEnum(Enum):
    AMBIENT = 0
    COMBAT = 1
    MUSIC = 2
    # I'm sure there will be more


class MaterialEnum(Enum):
    STONE = auto()
    WOOD = auto()
    GRASS = auto()
    DIRT = auto()
    SNOW = auto()
