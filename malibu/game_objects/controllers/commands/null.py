from ....typing import IControllerCommand, IInputHandler


class NullCommand(IControllerCommand):
    def execute(self, actor: IInputHandler) -> None:
        pass
