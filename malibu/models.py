from dataclasses import dataclass, replace
from typing import Dict, Optional, Tuple, List, Union

from .const import DEFAULT_AUDIO_DISTANCE
from .enum import AudioTypeEnum, AudioCategoryEnum


@dataclass
class MapSpec:

    name: str
    path: str
    music: str

    def __repr__(self):
        return f"<MapSpec({self.name}:{self.path})>"

    @classmethod
    def parse(cls, dat: Dict[str, any]) -> "MapSpec":
        return MapSpec(
            name=dat["name"],
            path=dat["path"],
            music=dat["music"])


@dataclass
class AudioSpec:

    name: str
    path: str
    type: AudioTypeEnum
    category: AudioCategoryEnum
    distance: int
    gain: float

    def __repr__(self):
        return f"<AudioSpec({self.name}:{self.type.name}:{self.path})>"

    @classmethod
    def parse(cls, dat: Dict[str, any]) -> "AudioSpec":
        return AudioSpec(
            name=dat["name"],
            path=dat["path"],
            type=AudioTypeEnum[dat["type"]],
            category=AudioCategoryEnum[dat["category"]],
            distance=dat.get("distance", DEFAULT_AUDIO_DISTANCE),
            gain=max(0.0, min(1.0, dat.get("gain", 1.0))))


@dataclass
class ObjectSpec:

    name: str
    path: str

    def __repr__(self):
        return f"<ObjectSpec({self.name}:{self.path}>)"

    @classmethod
    def parse(cls, dat: Dict[str, any]) -> "ObjectSpec":
        return ObjectSpec(
            name=dat["name"],
            path=dat["path"])


@dataclass
class ObjectData:

    tags: List[str]
    components: Dict[str, Union[List[str], Dict[str, any]]]

    @classmethod
    def parse(cls, dat: Dict[str, any]) -> "ObjectData":
        return ObjectData(
            tags=dat["Tags"],
            components=dat["Components"])
