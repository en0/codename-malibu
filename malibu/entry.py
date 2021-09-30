import pygame
from .ioc import get_game


def main():
    game = get_game()
    game.play()



if __name__ == "__main__":
    pygame.init()
    main()
