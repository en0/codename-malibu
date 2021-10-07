from malibu_lib.abc import GameSprite


class CampfireSprite(GameSprite):

    sprite_name = "campfire"

    def on_toggle(self):
        self.active_animation = "lit"

    def initialize(self, **kwargs) -> None:
        x, y = kwargs.get("position", (0, 0))
        # Adjust the location to compensate for the
        # map editors coordinate system
        self.position = (x + 8, y + 16)
