from typing import Dict, Tuple, Optional, List

import pkg_resources
from pygame import Surface, image, Rect
from logging import getLogger
from yaml import safe_load

from .model import SpriteSpec, SpriteSheetSpec
from .typing import IAssetManager


_log = getLogger(__name__)
SpriteSheetEntry = Tuple[SpriteSheetSpec, Optional[List[Surface]]]
SpriteSpecEntry = Tuple[str, Optional[SpriteSpec]]


class StructuredAssetManager(IAssetManager):

    def get_sprite_spec(self, sprite_name: str) -> SpriteSpec:
        path, spec = self._sprite_specs[sprite_name]
        if spec is None:
            with pkg_resources.resource_stream(self._package, path) as fd:
                dat = safe_load(fd)
                spec = SpriteSpec.load(dat)
                self._sprite_specs[sprite_name] = (path, spec)
        return spec

    def get_sprite_sheet(self, sheet_name: str) -> List[Surface]:
        spec, tiles = self._sprite_sheets[sheet_name]
        if tiles is None:
            tiles = self._load_tiles(spec)
            self._sprite_sheets[sheet_name] = (spec, tiles)
        return tiles

    def get_sprite_sheet_tile(self, sheet_name: str, id: int) -> Surface:
        _log.debug("Fetching tile: %s[%s]", sheet_name, id)
        tiles = self.get_sprite_sheet(sheet_name)
        return tiles[id]

    def clear(self) -> None:
        _log.info("Clearing loaded assets")
        self._sprite_specs = {k: (p, None) for k, p in self._sprite_specs.items()}
        self._sprite_sheets = {k: (p, None) for k, p in self._sprite_sheets.items()}

    def _load_tiles(self, spec: SpriteSheetSpec) -> List[Surface]:

        _log.info("Loading tile sheet: %s:%s", self._package, spec.path)

        path = pkg_resources.resource_filename(self._package, spec.path)
        _log.debug("Full tile sheet path: %s", path)

        sprite_sheet = image.load(path)
        width, height = sprite_sheet.get_size()
        tile_width, tile_height = spec.tile_size
        _log.debug(
            "Attempting to parse tile sheet: TotalSize=(%s, %s), TileSize=(%s, %s)",
            width, height, tile_width, tile_height
        )

        ret = []
        for h in range(height // tile_height):
            for w in range(width // tile_width):
                tile_rec = Rect(w * tile_width, h * tile_height, tile_width, tile_height)
                tile = sprite_sheet.subsurface(tile_rec)
                ret.append(tile)

        _log.debug("Loaded %s tile from %s:%s", len(ret), self._package, spec.path)
        return ret

    def __init__(self, package: str) -> None:

        self._package = package
        with pkg_resources.resource_stream(self._package, "assets/index.yaml") as fp:
            index = safe_load(fp)

        self._sprite_sheets: Dict[str, SpriteSheetEntry] = {
            x["name"]: (SpriteSheetSpec.load(x), None)
            for x in index["sprite-sheets"]
        }

        self._sprite_specs: Dict[str, SpriteSpecEntry] = {
            x["name"]: (x["path"], None)
            for x in index["sprite-specs"]
        }

