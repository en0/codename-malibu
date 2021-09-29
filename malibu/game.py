from malibu_lib.abc import GameABC


class MalibuGame(GameABC):

    x = 0

    def startup(self) -> None:
        ...

    def shutdown(self) -> None:
        ...

    def update(self, frame_delta: int) -> None:
        self.x += 1
        if self.x % 100 == 0:
            print(self.x)

        if self.x == 100:
            print("Going full screen")
            settings = self.settings_manager.get_settings()
            settings.video_settings.full_screen = True
            self.settings_manager.set_settings(settings)

        if self.x == 300:
            print("Going NOT full screen")
            settings = self.settings_manager.get_settings()
            settings.video_settings.full_screen = False
            self.settings_manager.set_settings(settings)

        if self.x == 500:
            self.close()
