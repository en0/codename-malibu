import pygame

from .game import MalibuGame
from .scene import NoOpScene
from malibu_lib.typing import IGame
from malibu_lib.model import GameSettings, VideoSettings


def main():
    game: IGame = MalibuGame()
    game.set_scene(NoOpScene())
    game.reconfigure(GameSettings(
        video_settings=VideoSettings(),
        input_settings={
            "attack": ("key", pygame.K_SPACE),
            "inventory": ("mouse", pygame.BUTTON_LEFT),
        }
    ))
    game.play()


if __name__ == "__main__":
    pygame.init()
    main()
