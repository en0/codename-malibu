import pygame
from . import factory


def main():
    game = factory.get_game()
    game.play()



if __name__ == "__main__":
    pygame.init()
    main()
