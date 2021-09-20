import logging
import pygame
from argparse import ArgumentParser

from malibu_lib import StructuredAssetManager

from .sprite_viewer import SpriteViewer

logging.basicConfig(level="INFO")


def run_sprite_viewer(opts):
    pygame.init()
    asset_manager = StructuredAssetManager(opts.asset_package)
    print(opts)
    sv = SpriteViewer(opts.sprite_name, asset_manager)
    sv.run()


def get_opts():
    ap = ArgumentParser()
    sp = ap.add_subparsers(help='foo')

    ap_sv = sp.add_parser("sprite-viewer")
    ap_sv.add_argument("--asset-package", type=str, default="malibu")
    ap_sv.add_argument("sprite_name", type=str, default="malibu")
    ap_sv.set_defaults(fn=run_sprite_viewer)
    return ap.parse_args()


def main():
    opts = get_opts()
    opts.fn(opts)


if __name__ == "__main__":
    main()
