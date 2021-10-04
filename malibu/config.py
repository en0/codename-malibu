import pygame
from malibu_lib.model import GameConfig, GameSettings, VideoSettings

game_config = GameConfig(

    author="ian.laird",
    name="malibu",
    version="0.0.2",
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
            "full_screen": ("key", pygame.K_F11),
            "run-up": ("key", pygame.K_w),
            "run-left": ("key", pygame.K_a),
            "run-right": ("key", pygame.K_d),
            "run-down": ("key", pygame.K_s),
            "attack": ("key", pygame.K_SPACE),
            "inventory": ("key", pygame.K_e),
        }
    )
)
