from malibu_lib.abc import GameSprite


class ChestSprite(GameSprite):

    sprite_name = "chest"

    def toggle(self):
        if self.active_animation == "opened":
            self.active_animation = "closed"
        else:
            self.active_animation = "opened"

    def initialize(self, **kwargs) -> None:
        self.position = kwargs.get("position", (0, 0))
