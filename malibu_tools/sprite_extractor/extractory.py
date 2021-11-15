import pygame
from typing import Tuple, List


class SpriteExtractor:

    def extract(self):
        tiles = self._gather_tiles()
        surf = self._write_tiles(tiles)
        pygame.image.save_extended(surf, self.out_file)

    def _write_tiles(self, tiles: List[pygame.Surface]):
        surf = pygame.Surface(self.out_size)
        surf.fill(self.color_key)
        tile_width, tile_height = self.tile_size
        total_width, _ = self.out_size
        tiles_per_row = total_width // tile_width
        for i, tile in enumerate(tiles):
            x = (i % tiles_per_row) * tile_width
            y = (i // tiles_per_row) * tile_height
            rect = pygame.Rect(x, y, tile_width, tile_height)
            surf.blit(tile, rect)
        return surf

    def _gather_tiles(self):
        tiles = []
        tile_width, tile_height = self.tile_size
        surf = pygame.image.load(self.in_file)
        total_width, _ = surf.get_size()
        tiles_per_row = total_width // tile_width
        for i in self.in_map:
            x = (i % tiles_per_row) * tile_width
            y = (i // tiles_per_row) * tile_height
            rect = pygame.Rect(x, y, tile_width, tile_height)
            tiles.append(surf.subsurface(rect))
        return tiles

    def __init__(self,
                 color_key: Tuple[int, int, int],
                 in_file: str,
                 out_file: str,
                 tile_size: Tuple[int, int],
                 out_size: Tuple[int, int],
                 in_map: List[int],
                 ):
        (x, y), (tx, ty) = out_size, tile_size
        self.out_size = (x*tx, y*ty)
        self.tile_size = tile_size
        self.out_file = out_file
        self.in_file = in_file
        self.in_map = in_map
        self.color_key = color_key
