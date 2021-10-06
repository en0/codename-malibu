from malibu_lib.abc import GameSprite


class CampfireSprite(GameSprite):

    sprite_name = "campfire"

    def initialize(self, **kwargs) -> None:
        self.position = kwargs.get("position", (0, 0))

    def lite(self):
        self.active_animation = "lit"
