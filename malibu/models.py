import pygame
from pygame import Surface, Vector2
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
class ObjectDataComponentSpec:

    klass: str
    args: List[any]
    kwargs: Dict[str, any]

    @classmethod
    def parse(cls, data: Dict[str, any]) -> "ObjectDataComponentSpec":
        return ObjectDataComponentSpec(
            klass=data["class"],
            args=data.get("args", []),
            kwargs=data.get("kwargs", {}),
        )


@dataclass
class ObjectData:

    tags: List[str]
    input_component: ObjectDataComponentSpec
    behavior_components: List[ObjectDataComponentSpec]
    graphics_component: ObjectDataComponentSpec

    @classmethod
    def parse(cls, data: Dict[str, any]) -> "ObjectData":
        return ObjectData(
            tags=data["tags"],
            input_component=ObjectDataComponentSpec.parse(data["input-component"]),
            graphics_component=ObjectDataComponentSpec.parse(data["graphics-component"]),
            behavior_components=[
                ObjectDataComponentSpec.parse(spec)
                for spec in data["behavior-components"]
            ]
        )


@dataclass
class AnimationFrameSpec:
    index: int
    sprite_sheet: str
    frame_delay: int
    footprint: Tuple[float, float, float, float]
    bounding_box: Tuple[float, float, float, float]

    @classmethod
    def parse(cls, data: Dict[str, any], **defaults) -> "AnimationFrameSpec":
        fp_x, fp_y, fp_w, fp_h = data.get("footprint", defaults.get("footprint", "0,0,0,0")).split(",")
        bb_x, bb_y, bb_w, bb_h = data.get("bounding-box", defaults.get("bounding-box", "0,0,0,0")).split(",")
        return AnimationFrameSpec(
            index=data["index"],
            sprite_sheet=data.get("sprite-sheet", defaults.get("sprite-sheet")),
            frame_delay=data.get("frame-delay", defaults.get("frame-delay")),
            footprint=(float(fp_x), float(fp_y), float(fp_w), float(fp_h)),
            bounding_box=(float(bb_x), float(bb_y), float(bb_w), float(bb_h)),
        )


@dataclass
class AnimationSpec:
    name: str
    repeat: int
    frames: List[AnimationFrameSpec]

    @classmethod
    def parse(cls, data: Dict[str, any], **defaults) -> "AnimationSpec":
        defaults.update(data)
        return AnimationSpec(
            name=data["name"],
            repeat=data.get("repeat", defaults.get("repeat", 0)),
            frames=[AnimationFrameSpec.parse(f, **defaults) for f in data["frames"]]
        )


@dataclass
class SpriteSheetSpec:

    name: str
    path: str
    tile_size: Tuple[int, int]

    def __repr__(self):
        return f"<SpriteSheetSpec({self.name}:{self.path}>)"

    @classmethod
    def parse(cls, dat: Dict[str, any]) -> "SpriteSheetSpec":
        w, h = dat["tile-size"].split(",")
        return SpriteSheetSpec(
            name=dat["name"],
            path=dat["path"],
            tile_size=(int(w), int(h)))
