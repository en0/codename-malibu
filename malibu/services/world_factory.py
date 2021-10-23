from pytmx import load_pygame

from ..mixins import AssetMixin
from ..typing import IWorldFactory, IWorldMap
from ..lib import WorldMap


class MapFactory(AssetMixin, IWorldFactory):
    def build_world(self, name: str) -> IWorldMap:
        spec = self.asset_manager.get_map_spec(name)
        tiled_map = load_pygame(spec.path)
        ret = WorldMap(tiled_map, spec.music)
        ret.initialize()
        return ret
