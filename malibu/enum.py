from enum import Enum, auto


class CameraTypeEnum(Enum):
    STATIC = auto()
    DYNAMIC = auto()


class ComponentMessageEnum(Enum):
    SET_VELOCITY = auto()
    SET_LOCATION = auto()
    SET_BOUNDING_BOX = auto()


class GameObjectEnum(Enum):
    HERO = auto()


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
    STONE: auto()
    WOOD: auto()
    GRASS: auto()
    DIRT: auto()
    SNOW: auto()