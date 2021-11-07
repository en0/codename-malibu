from pygame import draw, Rect, Vector2, Surface
from pytmx import TiledMap, TiledTileLayer
from typing import List, Optional, Dict, Tuple, Union, NamedTuple, Generator, Callable, Iterable, Set

from .quad_tree import QuadTree
from ..enum import MaterialEnum, GameObjectMessageEnum
from ..mixins import AudioMixin, ObjectFactoryMixin
from ..typing import IWorldMap, IGameObject, IGraphicsService, IKeyboardService, IDataComponent


def get_object_sort_value(obj: IGameObject):
    location = obj.data.location
    if location is None:
        return 0
    return location.y


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


class DummyObjectComponent(NamedTuple):
    location: Vector2


class DummyObject:

    @property
    def data(self):
        return self._component

    def render(self, gfx: IGraphicsService):
        gfx.blit(self._img, self._rect)

    def __init__(self, img: Surface, rect: Rect, zheight: int):
        self._img = img
        self._rect = rect
        x, y = self._rect.midbottom
        self._component = DummyObjectComponent(location=Vector2(x, y + zheight))


class WorldMap(AudioMixin, ObjectFactoryMixin, IWorldMap):

    def objects(self) -> Iterable[IGameObject]:
        return self.find_game_objects(lambda x: True)

    def find_game_objects(self, predicate: Callable[[IGameObject], bool] = None) -> Iterable[IGameObject]:
        return filter(predicate or True, self._game_objects)

    def find_first_game_objects(self, predicate: Callable[[IGameObject], bool] = None) -> Optional[IGameObject]:
        return next(filter(predicate or True, self._game_objects), None)

    def get_rect(self) -> Rect:
        return self._map_rect.copy()

    def get_default_music(self) -> str:
        return self._default_music

    def render(self, gfx: IGraphicsService) -> None:


        # We need to pull out the "foreground" tiles. These need to be
        # Sorted into the game object list so the world is layered correctly
        # This will put the player behind or infront of things like trees and bushes
        foreground_tiles = []

        # We will use the viewport to get only the tiles in the visible area
        vp = gfx.get_viewport()

        for desc in self._tiles.hit(gfx.get_viewport()):
            for gid in desc.get_gids():
                if gid in self._animation_map:
                    gid = self._animation_map[gid].gid
                img = self._tiled_map.get_tile_image_by_gid(gid)
                if gid in self._foreground_map:
                    # This img needs to be sorted into the object list
                    foreground_tiles.append(DummyObject(img, desc.rect, self._foreground_map[gid]))
                else:
                    gfx.blit(img, desc.rect)

        # Sort all the game objects by the y axis to layer the forground
        objects = sorted(
            self._game_objects + foreground_tiles,
            key=lambda o: get_object_sort_value(o))
        for obj in objects:
            obj.render(gfx)

    def update(self, frame_delta: float) -> None:
        for name, point in self._tile_sounds:
            self.audio.enqueue(name, point)
        for desc in self._animation_map.values():
            desc.update(frame_delta)
        for obj in self._game_objects:
            obj.update(frame_delta, self)

    def is_walkable(self, rect: Rect) -> bool:
        if not self._map_rect.contains(rect):
            return False
        tiles: List[TileDescription] = self._tiles.hit(rect)
        return all(map(lambda x: x.is_walkable, tiles))

    def get_material(self, rect: Rect) -> MaterialEnum:
        tiles: List[TileDescription] = self._tiles.hit(rect)
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
        self._foreground_map = {}
        for key in self._tiled_map.gidmap.keys():
            props = self._tiled_map.get_tile_properties_by_gid(key)
            mat = props.get("material")
            prop_map[key] = (
                props.get("walkable"),
                MaterialEnum[mat.upper()] if mat else None,
                props.get("sound"),
            )
            if "frames" in props and props["frames"]:
                self._animation_map[key] = GidAnimationDescription(props["frames"])
            if props.get("foreground", False):
                self._foreground_map[key] = props.get("z-height", 0) * self._tiled_map.tileheight

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

        # Load game objects
        self._game_objects = []
        for map_object in self._tiled_map.objects:
            game_object = self.object_factory.new(map_object.name)
            location = Vector2(map_object.x, map_object.y)
            game_object.data.location = location
            self._game_objects.append(game_object)

        self._tiles = QuadTree([x for x in all_tiles], bounding_rect=self._map_rect)

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
        self._tiles: QuadTree = None
        self._map_rect: Rect = Rect(0, 0, 0, 0)
        self._tile_sounds: Tuple[str, Vector2] = []
        self._animation_map: Dict[int, GidAnimationDescription] = {}
        self._foreground_map: Dict[int, int] = {}
        self._game_objects: List[IGameObject] = []
