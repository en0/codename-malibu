from dataclasses import dataclass
from enum import Enum
from pygame import draw, Rect, Surface, Vector2
from pytmx import TiledMap, TiledTileLayer, load_pygame
from typing import List, Optional, Dict, Tuple, Union

from ..enum import MaterialEnum
from ..mixins import AudioMixin
from ..quad_tree import QuadTree
from ..typing import IWorldMap, IGameObject
from ..mixins import AssetMixin
from ..typing import IWorldFactory, IWorldMap


class MapFactory(AssetMixin, IWorldFactory):

    def build_world(self, name: str) -> IWorldMap:
        spec = self.asset_manager.get_map_spec(name)
        tiled_map = load_pygame(spec.path)
        ret = WorldMap(tiled_map, spec.music)
        ret.initialize()
        return ret


class TileLayerTypeEnum(Enum):
    DYNAMIC: 0
    STATIC: 1


@dataclass
class LayerAnimationDesc:
    frame_durations: List[int]
    remaining_duration: int
    current_frame: int

    @property
    def frame_count(self) -> int:
        return len(self.frame_durations)

    def update(self, frame_delta: float):
        frame_delta *= 1000
        self.remaining_duration -= frame_delta
        if self.remaining_duration <= 0:
            self.current_frame = (self.current_frame + 1) % self.frame_count
            self.remaining_duration = self.frame_durations[self.current_frame]


@dataclass
class TileDescription:
    rect: Rect
    is_walkable: bool
    material: Optional[MaterialEnum]
    tiles: List[Union[int, str]]
    anim: Dict[str, List[int]]

    def __hash__(self):
        return hash(tuple(self.tiles))

    def __repr__(self):
        return (
            "<Tile "
            f"rect={self.rect} "
            f"tiles={self.tiles} "
            f"walkable={self.is_walkable} "
            f"material={self.material} "
            ">"
        )

    @staticmethod
    def new(rect: Rect):
        return TileDescription(
            rect=rect,
            is_walkable=True,
            material=None,
            tiles=[],
            anim={})


class WorldMap(AudioMixin, IWorldMap):

    show_sound = False

    def get_sprites(self) -> List[IGameObject]:
        return []

    def get_rect(self) -> Rect:
        return self._map_rect.copy()

    def get_default_music(self) -> str:
        return self._default_music

    def render(self, gfx: Surface, rect: Rect) -> None:
        for desc in self._qtree.hit(rect):
            for gid in desc.tiles:
                if isinstance(gid, int):
                    image = self._tiled_map.get_tile_image_by_gid(gid)
                else:
                    # GID in this case is the animation name
                    frame = self._layer_animations[gid].current_frame
                    _gid = desc.anim[gid][frame]
                    image = self._tiled_map.get_tile_image_by_gid(_gid)
                gfx.blit(image, desc.rect)
            # Show tile border
            #draw.rect(gfx, (100, 0, 0), desc.rect, width=1)

        if self.show_sound:
            # Show audio sources
            for sound, point in self._sounds:
                draw.circle(gfx, (0, 0, 100), point, radius=8)

    def update(self, frame_delta: float) -> None:
        for name, point in self._sounds:
            self.audio.enqueue(name, point)
        for desc in self._layer_animations.values():
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

    def add_ambience(self, sound_name: str, point: Vector2):
        self._sounds.append((sound_name, point))

    def initialize(self) -> None:
        self._map_rect = Rect(
            0, 0,
            self._tiled_map.width * self._tiled_map.tilewidth,
            self._tiled_map.height * self._tiled_map.tileheight,
        )
        for (x, y), tile in self._collect_tiles().items():
            rect = self._as_rect(x, y)
            desc = TileDescription.new(rect)
            self._tiles.append(desc)
            for layer, gid in tile:
                props = self._tiled_map.get_tile_properties_by_gid(gid)

                # Add the tile_layers' sound to the map ambience.
                tile_sound = props.get("sound")
                if tile_sound is not None:
                    self.add_ambience(tile_sound, Vector2(*rect.center))

                # Flatten the tile layers into  single set of attributes.
                desc.material = props.get("material", desc.material)
                desc.is_walkable = props.get("walkable", desc.is_walkable)

                # Add the tile ids to the list of tiles to be rendered.
                if layer.visible and layer.properties.get("type") == "static":
                    desc.tiles.append(gid)

                elif layer.visible and layer.properties.get("type") == "dynamic":
                    # Add the details about the animation layer
                    grp = layer.properties.get("animation_group", "default")
                    dur_ms = layer.properties.get("frame_duration_ms", 500)
                    self._add_layer_animation(grp, dur_ms, len(desc.anim.get(grp, [])))
                    # Add the animation group to the tile list so the renderer has the ordering
                    if grp not in desc.anim:
                        desc.tiles.append(grp)
                    # Add the frame to the list of frames for this animation group
                    desc.anim.setdefault(grp, []).append(gid)

        self._qtree = QuadTree([x for x in self._tiles], bounding_rect=self._map_rect)

    def _as_rect(self, x: int, y: int) -> Rect:
        return Rect(
            x * self._tiled_map.tilewidth,
            y * self._tiled_map.tileheight,
            self._tiled_map.tilewidth,
            self._tiled_map.tileheight
        )

    def _add_layer_animation(self, grp_name: str, duration_ms: int, frame_number: int):
        # This will be called for each tile but we only want to track each layer
        desc = self._layer_animations.get(grp_name)
        if desc is None:
            desc = LayerAnimationDesc([], 0, 0)
            self._layer_animations[grp_name] = desc
        if desc.frame_count < frame_number + 1:
            desc.frame_durations.append(duration_ms)
            # Set the animation step on the last frame as expired
            desc.current_frame = frame_number

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
        self._tiles: List[TileDescription] = []
        self._layer_animations: Dict[str, LayerAnimationDesc] = {}
        self._sounds = []
        self._qtree: QuadTree = None
        self._map_rect: Rect = Rect(0, 0, 0, 0)
