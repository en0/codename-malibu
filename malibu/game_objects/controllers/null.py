from .commands import NullCommand
from ..component_base import ComponentBase
from ...typing import IWorldMap, IControllerSource, IControllerCommand, IControllerComponent


class NullController(ComponentBase, IControllerComponent, IControllerSource):

    def update(self, frame_delta: float, world: IWorldMap) -> None:
        pass

    def get_input(self) -> IControllerCommand:
        return self._null

    def __init__(self):
        self._null = NullCommand()
