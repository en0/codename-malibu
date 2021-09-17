from typing import Dict, List, IO
from dataclasses import dataclass
from yaml import safe_load


@dataclass
class AnimationFrameSpec:
    index: int
    sheet: str
    delay: int = 500
    mirror: bool = False
    flip: bool = False
    opacity: float = 1.0


@dataclass
class AnimationSpec:
    name: str
    type: str
    frames: List[AnimationFrameSpec]


@dataclass
class SpriteSpec:
    name: str
    desc: str
    animations: Dict[str, AnimationSpec]


def load_spec(stream: IO) -> SpriteSpec:
    """ Load a sprite specification from the given stream.

    Arguments:
        stream: A IO stream containing a sprite specification.

    Returns:
        A SpriteSpec filled with the data described in the given stream.

    Raises:
        KeyError if a required value is not provided in the specification.
        TypeError if a given field in the specification is the wrong type.
        ValueError if the sprite has a duplicate animation name.
    """

    # The data stream is a yaml file
    dat: dict = safe_load(stream)

    # Define the global defaults and set any that might be missing.
    defaults: dict = dat.get("defaults", {})
    defaults.setdefault("delay", 500)
    defaults.setdefault("mirror", False)
    defaults.setdefault("flip", False)
    defaults.setdefault("opacity", 1.0)

    # Parse each animation and it's frames
    anim_specs: Dict[str, AnimationSpec] = {}
    for anim_raw in dat["animations"]:

        # Don't allow duplicate names
        name = anim_raw["name"]
        if name in anim_specs:
            raise ValueError(
                f'Duplicate animation name "{name}". '
                'Animation names must be unique.'
            )

        # Defaults can be overriden at any level.
        scoped_defaults = defaults.copy()
        scoped_defaults.update(anim_raw)

        anim_specs[name] = AnimationSpec(
            name=anim_raw["name"],
            type=anim_raw["type"],
            frames=[
                AnimationFrameSpec(
                    index=int(frame_raw["index"]),
                    sheet=frame_raw.get("sheet", scoped_defaults["sheet"]),
                    delay=frame_raw.get("delay", scoped_defaults["delay"]),
                    mirror=frame_raw.get("mirror", scoped_defaults["mirror"]),
                    flip=frame_raw.get("flip", scoped_defaults["flip"]),
                    opacity=float(frame_raw.get("opacity", scoped_defaults["opacity"])),
                ) for frame_raw in anim_raw["frames"]
            ]
        )

    return SpriteSpec(dat["name"], dat.get("desc", ""), anim_specs)

