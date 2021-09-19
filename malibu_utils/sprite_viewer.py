from argparse import ArgumentParser
from os.path import join as join_path
from malibu_lib import StructuredAssetManager, BasicAnimation

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
    run_right = BasicAnimation(spec.animations["run-right"], asset_manager)
    run_left = BasicAnimation(spec.animations["run-left"], asset_manager)
    pygame.init()
    clock = pygame.time.Clock()
    _screen = pygame.display.set_mode((800, 600), pygame.HWACCEL | pygame.HWSURFACE)
    screen = pygame.Surface((200, 150))

    frame_delta = 0
    is_running = True
    while is_running:
        frame_delta = clock.tick(60)/1000.0
        run_right.update(frame_delta)
        run_left.update(frame_delta)
        screen.fill((0, 0, 0))
        screen.blit(run_right.image, (0, 0))
        screen.blit(run_left.image, (32, 0))

        _screen.blit(pygame.transform.scale(screen, _screen.get_size()), (0,0))
        pygame.display.flip()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                is_running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_d:
                run_left.reset()

if __name__ == "__main__":
    main()
