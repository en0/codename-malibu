from argparse import ArgumentParser
from os.path import join as join_path
from malibu_lib import StructuredAssetManager

import pygame
import logging

logging.basicConfig(level="DEBUG")


def get_opts():
    ap = ArgumentParser()
    ap.add_argument("--asset-package", type=str, default="malibu")
    ap.add_argument("SPRITE", type=str, help="The location of the sprite file to load.")
    return ap.parse_args()


def sprite_path(sprite_name):
    return join_path("assets", "sprites", f"{sprite_name}.yaml")


def sheet_path(sheet_name):
    ...


def main():
    opts = get_opts()
    asset_manager = StructuredAssetManager(opts.asset_package)
    spec = asset_manager.get_sprite_spec(opts.SPRITE)
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    tile = asset_manager.get_sprite_sheet_tile("base-boi-walk", 0)
    while not pygame.event.get(pygame.QUIT):
        screen.fill((0, 0, 0))
        screen.blit(tile, (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    main()
