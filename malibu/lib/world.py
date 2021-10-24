from dataclasses import dataclass
from enum import Enum
from pygame import draw, Rect, Vector2
from pytmx import TiledMap, TiledTileLayer, load_pygame
from typing import List, Optional, Dict, Tuple, Union, NamedTuple, Generator

from .quad_tree import QuadTree
from ..enum import MaterialEnum
from ..mixins import AudioMixin
from ..typing import IWorldMap, IGameObject, IGraphicsService


class AnimationFrame(NamedTuple):
    gid: int
    duration: int


class GidAnimationDescription:

    index: int
    duration: int
    frames: List[AnimationFrame]

    @property
    def gid(self) -> int:
        return self.frames[self.index].gid

    @property
    def frame(self) -> AnimationFrame:
        return self.frames[self.index]

    def update(self, frame_delta: float) -> None:
        self.duration -= (frame_delta * 1000)
        if self.duration <= 0:
            self.index = (self.index + 1) % len(self.frames)
            self.duration += self.frame.duration

    def __repr__(self):
        return "{}, {}, {}".format(self.index, self.duration, self.gid)

    def __init__(self, frames: List[AnimationFrame]) -> None:
        self.index = 0
        self.duration = frames[0].duration
        self.frames = frames.copy()


class TileDescription:

    rect: Rect
    is_walkable: bool
    material: Optional[MaterialEnum]

    def get_gids(self) -> Generator[int, None, None]:
        for tile in self._gids:
            if tile in self._animation_map:
                yield self._animation_map[tile].gid
            else:
                yield tile

    def add_gid(self, gid: int):
        self._gids.append(gid)

    def __hash__(self):
        return self._hash

    def __init__(self, rect: Rect, animation_map: Dict[int, GidAnimationDescription]):
        self.rect = rect
        self.is_walkable = True
        self.material = None
        self._hash = hash(tuple(rect))
        self._animation_map = animation_map
        self._gids: List[int] = []


class WorldMap(AudioMixin, IWorldMap):

    show_sound = False

    def get_sprites(self) -> List[IGameObject]:
        return []

    def get_rect(self) -> Rect:
        return self._map_rect.copy()

    def get_default_music(self) -> str:
        return self._default_music

    def render(self, gfx: IGraphicsService) -> None:

        vp = gfx.get_viewport()
        for desc in self._qtree.hit(gfx.get_viewport()):
            for gid in desc.get_gids():
                if gid in self._animation_map:
                    gid = self._animation_map[gid].gid
                img = self._tiled_map.get_tile_image_by_gid(gid)
                gfx.blit(img, desc.rect)

        if self.show_sound:
            # Show audio sources
            for sound, point in self._tile_sounds:
                abs_point = gfx.compute_absolute(point)
                draw.circle(gfx.get_hw_surface(), (0, 0, 100), abs_point, radius=8)

    def update(self, frame_delta: float) -> None:
        for name, point in self._tile_sounds:
            self.audio.enqueue(name, point)
        for desc in self._animation_map.values():
            desc.update(frame_delta)

    def is_walkable(self, rect: Rect) -> bool:
        if not self._map_rect.contains(rect):
            return False
        tiles: List[TileDescription] = self._qtree.hit(rect)
        return all(map(lambda x: x.is_walkable, tiles))

    def get_material(self, rect: Rect) -> MaterialEnum:
        tiles: List[TileDescription] = self._qtree.hit(rect)
        for tile in tiles:
            if tile.rect.collidepoint(rect.center):
                return tile.material
        return None

    def add_ambience(self, sound_name: str, point: Union[Vector2, Tuple[float, float]]):
        if sound_name is not None:
            self._tile_sounds.append((sound_name, Vector2(point)))

    def initialize(self) -> None:
        self._map_rect = Rect(
            0, 0,
            self._tiled_map.width * self._tiled_map.tilewidth,
            self._tiled_map.height * self._tiled_map.tileheight,
        )

        # Collect Properties for each GID. Collect Frames for each GID
        self._animation_map, prop_map = {}, {}
        for key in self._tiled_map.gidmap.keys():
            props = self._tiled_map.get_tile_properties_by_gid(key)
            prop_map[key] = (
                props.get("walkable"),
                props.get("material"),
                props.get("sound")
            )
            if "frames" in props and props["frames"]:
                self._animation_map[key] = GidAnimationDescription(props["frames"])

        # Create tile with each layer described in that tile
        all_tiles = []
        for (x, y), tile in self._collect_tiles().items():
            rect = self._as_rect(x, y)
            desc = TileDescription(rect, self._animation_map)
            all_tiles.append(desc)
            for layer, gid in tile:
                is_walkable, material, sound = prop_map[gid]
                desc.material = material or desc.material
                desc.is_walkable = is_walkable if is_walkable is not None else desc.is_walkable
                desc.add_gid(gid)
                self.add_ambience(sound, rect.center)

        self._qtree = QuadTree([x for x in all_tiles], bounding_rect=self._map_rect)

    def _as_rect(self, x: int, y: int) -> Rect:
        return Rect(
            x * self._tiled_map.tilewidth,
            y * self._tiled_map.tileheight,
            self._tiled_map.tilewidth,
            self._tiled_map.tileheight
        )

    def _collect_tiles(self) -> Dict[Tuple[int, int], List[Tuple[TiledTileLayer, int]]]:
        ret = {}
        for layer in self._tiled_map.layers:
            if not isinstance(layer, TiledTileLayer):
                continue
            for x, y, gid in layer:
                if gid != 0:
                    ret.setdefault((x, y), []).append((layer, gid))
        return ret

    def __init__(self, tiled_map: TiledMap, default_music_name: str) -> None:
        self._default_music = default_music_name
        self._tiled_map = tiled_map
        self._qtree: QuadTree = None
        self._map_rect: Rect = Rect(0, 0, 0, 0)
        self._tile_sounds: Tuple[str, Vector2] = []
        self._animation_map: Dict[int, GidAnimationDescription] = {}
