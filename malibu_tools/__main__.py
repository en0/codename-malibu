import logging
import pygame
from argparse import ArgumentParser

from .sprite_extractor import SpriteExtractor

logging.basicConfig(level="INFO")


def run_sprite_extractor(opts):
    pygame.init()
    SpriteExtractor(
        in_file=opts.INPUT_FILE,
        out_file=opts.OUTPUT_FILE,
        tile_size=tuple(opts.TILE_SIZE),
        out_size=tuple(opts.OUTPUT_SIZE),
        in_map=opts.MAP,
        color_key=opts.color_key
    ).extract()


def get_opts():
    ap = ArgumentParser()
    sp = ap.add_subparsers(help='foo')

    ap_ex = sp.add_parser("sprite-extractor")
    ap_ex.add_argument("--color-key", type=int, nargs=3, default=[255, 0, 255], help="Set the transparency key")
    ap_ex.add_argument("TILE_SIZE", type=int, nargs=2, help="The size of a single tile")
    ap_ex.add_argument("OUTPUT_SIZE", type=int, nargs=2, help="The number of tile in the x and y axis")
    ap_ex.add_argument("INPUT_FILE", type=str, help="The file to read tile from")
    ap_ex.add_argument("OUTPUT_FILE", type=str, help="A new file to write output to.")
    ap_ex.add_argument("MAP", type=int, nargs="*", help="Tile ID to read each input tile")
    ap_ex.set_defaults(fn=run_sprite_extractor)

    return ap.parse_args()


def main():
    opts = get_opts()
    opts.fn(opts)


if __name__ == "__main__":
    main()
