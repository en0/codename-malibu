from pytmx import load_pygame
from ..sprites import TileMap

from ..mixins import AssetMixin
from ..typing import IMapFactoryService, ITileMap


class MapFactoryService(AssetMixin, IMapFactoryService):

    def get_tile_map(self, name: str) -> ITileMap:
        spec = self.asset_manager.get_map_spec(name)
        tiled_map = load_pygame(spec.path)
        ret = TileMap(tiled_map, spec.music)
        ret.initialize()
        return ret
