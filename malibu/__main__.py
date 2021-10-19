import pygame

from malibu.services import ServiceLocator
from malibu.enum import SceneEnum

if __name__ == "__main__":
    pygame.init()
    ServiceLocator.install_default_providers()
    game = ServiceLocator.get_game()
    scene = ServiceLocator.get_scene_factory().new(SceneEnum.SPLASH)
    game.run(scene)
    pygame.quit()
