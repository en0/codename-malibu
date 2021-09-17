from typing import Dict, List, IO, Tuple
from dataclasses import dataclass


@dataclass
class AnimationFrameSpec:
    index: int
    sheet: str
    delay: int = 500
    mirror: bool = False
    flip: bool = False
    opacity: float = 1.0

    @staticmethod
    def load(dat: dict, **defaults) -> "AnimationFrameSpec":
        defaults.setdefault("delay", 500)
        defaults.setdefault("mirror", False)
        defaults.setdefault("flip", False)
        defaults.setdefault("opacity", 1.0)
        return AnimationFrameSpec(
            index=int(dat["index"]),
            sheet=dat.get("sheet", defaults["sheet"]),
            delay=dat.get("delay", defaults["delay"]),
            mirror=dat.get("mirror", defaults["mirror"]),
            flip=dat.get("flip", defaults["flip"]),
            opacity=float(dat.get("opacity", defaults["opacity"])),
        )


@dataclass
class AnimationSpec:
    name: str
    type: str
    frames: List[AnimationFrameSpec]

    @staticmethod
    def load(dat: dict, **defaults) -> "AnimationSpec":
        defaults.update(dat)
        return AnimationSpec(
            name=dat["name"],
            type=dat["type"],
            frames=[AnimationFrameSpec.load(x, **defaults) for x in dat["frames"]]
        )


@dataclass
class SpriteSpec:
    name: str
    desc: str
    animations: Dict[str, AnimationSpec]

    @staticmethod
    def load(dat: dict) -> "SpriteSpec":
        # Define the global defaults and set any that might be missing.
        defaults: dict = dat.get("defaults", {})
        return SpriteSpec(
            name=dat["name"],
            desc=dat["desc"],
            animations={a.name: a for a in map(lambda x: AnimationSpec.load(x, **defaults), dat["animations"])}
        )



@dataclass
class SpriteSheetSpec:
    name: str
    path: str
    tile_size: Tuple[int, int]

    @staticmethod
    def load(dat: dict) -> "SpriteSheetSpec":
        return SpriteSheetSpec(
            name=dat["name"],
            path=dat["path"],
            tile_size=(dat["tile-width"], dat["tile-height"]),
        )
