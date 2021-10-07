from pygame import Rect
from typing import Dict, List, IO, Tuple, Set, NamedTuple
from dataclasses import dataclass, asdict


def _spec2rect(spec: Dict[str, str]):
    width, height = [int(x.strip(" ")) for x in spec["size"].split(",")]
    x, y = [int(x.strip(" ")) for x in spec["offset"].split(",")]
    return Rect(x, y, width, height)


@dataclass
class AnimationFrameSpec:
    index: int
    sheet: str
    delay: int
    mirror: bool
    flip: bool
    opacity: int
    rotation: int
    scale_height: float
    scale_width: float
    footprint: Rect
    boundary: Rect

    @staticmethod
    def load(dat: dict, **defaults) -> "AnimationFrameSpec":
        defaults.setdefault("delay", 500)
        defaults.setdefault("mirror", False)
        defaults.setdefault("flip", False)
        defaults.setdefault("opacity", 1.0)
        defaults.setdefault("rotation", 0)
        defaults.setdefault("scale-width", 1)
        defaults.setdefault("scale-height", 1)
        return AnimationFrameSpec(
            index=int(dat["index"]),
            sheet=dat.get("sheet", defaults["sheet"]),
            delay=dat.get("delay", defaults["delay"]),
            mirror=dat.get("mirror", defaults["mirror"]),
            flip=dat.get("flip", defaults["flip"]),
            opacity=int(dat.get("opacity", defaults["opacity"])),
            rotation=int(dat.get("rotation", defaults["rotation"])),
            scale_width=float(dat.get("scale-width", defaults["scale-width"])),
            scale_height=float(dat.get("scale-height", defaults["scale-height"])),
            footprint=_spec2rect(dat.get("footprint", defaults["footprint"])),
            boundary=_spec2rect(dat.get("boundary", defaults["boundary"])),
        )


@dataclass
class AnimationSpec:

    name: str
    repeat: int
    frames: List[AnimationFrameSpec]
    flags: Set[str]

    @staticmethod
    def load(dat: dict, **defaults) -> "AnimationSpec":
        defaults.update(dat)
        return AnimationSpec(
            name=dat["name"],
            repeat=dat.get("repeat", -1),
            frames=[AnimationFrameSpec.load(x, **defaults) for x in dat["frames"]],
            flags={x for x in dat.get("flags",[])}
        )


@dataclass
class SpriteSpec:
    name: str
    desc: str
    animations: Dict[str, AnimationSpec]
    default_animation: str

    @staticmethod
    def load(dat: dict) -> "SpriteSpec":
        # Define the global defaults and set any that might be missing.
        defaults: dict = dat.get("defaults", {})
        return SpriteSpec(
            name=dat["name"],
            desc=dat["desc"],
            animations={a.name: a for a in map(lambda x: AnimationSpec.load(x, **defaults), dat["animations"])},
            default_animation=dat["default_animation"]
        )


@dataclass
class SpriteSheetSpec:
    name: str
    path: str
    tile_size: Tuple[int, int]
    color_key: Tuple[int, int, int]

    @staticmethod
    def load(dat: dict) -> "SpriteSheetSpec":
        color_key = dat.get("color-key")
        if color_key:
            color_key = [int(x.strip(" ")) for x in color_key.split(",")]
        return SpriteSheetSpec(
            name=dat["name"],
            path=dat["path"],
            tile_size=(dat["tile-width"], dat["tile-height"]),
            color_key=color_key,
        )


@dataclass
class VideoSettings:
    frame_rate: int = 60
    resolution: Tuple[int, int] = 800, 600
    viewport: Tuple[int, int] = 800, 600
    full_screen: bool = False
    double_buffer: bool = True
    hardware_accel: bool = True
    open_gl: bool = False

    @staticmethod
    def load(dat: dict) -> "VideoSettings":
        return VideoSettings(**dat)


@dataclass
class GameSettings:
    video_settings: VideoSettings
    input_settings: Dict[str, Tuple[str, int]]

    def todict(self):
        return asdict(self)

    @staticmethod
    def load(dat: dict) -> "GameSettings":
        return GameSettings(
            video_settings=VideoSettings.load(dat.get("video_settings", {})),
            input_settings=dat.get("input_settings", {}))


class GameConfig(NamedTuple):
    author: str
    name: str
    version: str
    asset_module: str
    default_settings: GameSettings
