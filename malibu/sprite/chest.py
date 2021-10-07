from malibu_lib.abc import GameSprite


class ChestSprite(GameSprite):

    sprite_name = "chest"

    def on_toggle(self):
        if self.active_animation == "opened":
            self.active_animation = "closed"
        else:
            self.active_animation = "opened"

    def initialize(self, **kwargs) -> None:
        x, y = kwargs.get("position", (0, 0))
        # Adjust the location to compensate for the
        # map editors coordinate system
        self.position = (x + 8, y + 16)
