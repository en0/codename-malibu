from ..typing import IGameScene, IGameInput, ISettingManager
from ..mixin import EventListenerMixin, EventPublisherMixin


class SceneABC(EventListenerMixin, EventPublisherMixin, IGameScene):

    @property
    def game_input(self) -> IGameInput:
        return self._game_input

    @property
    def settings_manager(self) -> ISettingManager:
        return self._settings_manager

    def __init__(
        self,
        game_input: IGameInput,
        settings_manager: ISettingManager,
    ) -> None:
        self._game_input = game_input
        self._settings_manager = settings_manager
