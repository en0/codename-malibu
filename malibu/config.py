import pygame
from malibu_lib.model import GameConfig, GameSettings, VideoSettings

from . import kb


game_config = GameConfig(
    author="ian.laird",
    name="malibu",
    version="0.0.4",
    asset_module="malibu",

    # If you changes are required,
    # you must change the version above
    default_settings=GameSettings(
        VideoSettings(
            frame_rate=60,
            resolution=(800, 600),
            viewport=(400, 300),
            full_screen=False,
            double_buffer=True,
            hardware_accel=True,
            open_gl=False,
        ),
        input_settings={
            kb.FULL_SCREEN: ("key", pygame.K_F11),
            kb.MOVE_UP: ("key", pygame.K_w),
            kb.MOVE_LEFT: ("key", pygame.K_a),
            kb.MOVE_RIGHT: ("key", pygame.K_d),
            kb.MOVE_DOWN: ("key", pygame.K_s),
            kb.ATTACK: ("key", pygame.K_SPACE),
            kb.INVENTORY: ("key", pygame.K_e),
        }
    )
)
