from malibu_lib.abc import GameSprite


class PlayerSprite(GameSprite):

    sprite_name = "base-boi"

    def initialize(self, **kwargs) -> None:
        self.position = kwargs.get("position", (0, 0))
