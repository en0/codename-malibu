import logging
import pygame
from argparse import ArgumentParser

from malibu_lib import StructuredAssetManager

from .sprite_viewer import SpriteViewer

logging.basicConfig(level="DEBUG")


def run_sprive_viewer(opts):
    pygame.init()
    asset_manager = StructuredAssetManager(opts.asset_package)
    sv = SpriteViewer(asset_manager)
    sv.run()


def get_opts():
    ap = ArgumentParser()
    sp = ap.add_subparsers(help='foo')

    ap_sv = sp.add_parser("sprite-viewer")
    ap_sv.add_argument("--asset-package", type=str, default="malibu")
    ap_sv.set_defaults(fn=run_sprive_viewer)
    return ap.parse_args()


def main():
    opts = get_opts()
    opts.fn(opts)
    #spec = asset_manager.get_sprite_spec(opts.SPRITE)
    #run_right = BasicAnimation(spec.animations["run-right"], asset_manager)
    #run_left = BasicAnimation(spec.animations["run-left"], asset_manager)
    #pygame.init()
    #clock = pygame.time.Clock()
    #_screen = pygame.display.set_mode((1024, 768), pygame.HWACCEL | pygame.HWSURFACE)
    ##screen = pygame.Surface((600, 450))
    #screen = pygame.Surface((200, 150))

    #window_manager = pygame_gui.UIManager((1024, 768))

    #tmap_path = pkg_resources.resource_filename(opts.asset_package, "assets/world/demo-map.tmx")
    #tmap = load_pygame(tmap_path)

    #pygame_gui.elements.UIButton(pygame.Rect(0, 0, 100, 40), "Hello, world", window_manager)

    #frame_delta = 0
    #is_running = True
    #while is_running:
    #    frame_delta = clock.tick(60)/1000.0

    #    for e in pygame.event.get():
    #        if e.type == pygame.QUIT:
    #            is_running = False
    #        if e.type == pygame.KEYDOWN and e.key == pygame.K_d:
    #            run_left.reset()

    #        window_manager.process_events(e)
    #    window_manager.update(frame_delta)
    #    run_right.update(frame_delta)
    #    run_left.update(frame_delta)

    #    screen.fill((0, 0, 0))
    #    # Render Map
    #    #for layer in tmap:
    #    #    for x, y, img in layer.tiles():
    #    #        screen.blit(img, (x*32, y*32))
    #    screen.blit(run_right.image, (0, 0))
    #    _screen.blit(pygame.transform.scale(screen, _screen.get_size()), (0,0))
    #    window_manager.draw_ui(_screen)
    #    pygame.display.flip()

if __name__ == "__main__":
    main()
