from pyioc3 import StaticContainerBuilder, Container, ScopeEnum
from pyioc3.interface import ContainerBuilder
from pygame.time import Clock

from .model import GameConfig
from .game_input import GameInput
from .setting_manager import YamlSettingsManager
from .path_provider import UserPathProvider
from .typing import (
    IGameInput,
    IGameScene,
    ISettingManager,
    IPathProvider,
    IGameSceneFactory,
)


class ContainerBuilderFacade(ContainerBuilder):

    def bind_factory(self, annotation, factory) -> None:
        self._bindings[annotation] = lambda: self._ioc.bind_factory(annotation, factory)

    def bind_constant(self, annotation, value) -> None:
        self._bindings[annotation] = lambda: self._ioc.bind_constant(annotation, value)

    def bind(
        self,
        annotation,
        implementation,
        scope: ScopeEnum = ScopeEnum.TRANSIENT,
        on_activate = None,
    ) -> None:
        self._bindings[annotation] = lambda: self._ioc.bind(annotation, implementation, scope, on_activate)

    def build(self) -> Container:
        for key, fn in self._bindings.items():
            fn()
        return self._ioc.build()

    def bind_defaults(self, config: GameConfig) -> None:

        self.bind_constant(
            annotation=GameConfig,
            value=config)

        self.bind_factory(
            annotation=IGameSceneFactory,
            factory=lambda x: lambda y: x.get(y))

        self.bind(
            annotation=Clock,
            implementation=Clock)

        self.bind(
            annotation=IPathProvider,
            implementation=UserPathProvider,
            scope=ScopeEnum.SINGLETON)

        self.bind(
            annotation=ISettingManager,
            implementation=YamlSettingsManager,
            scope=ScopeEnum.SINGLETON)

        self.bind(
            annotation=IGameInput,
            implementation=GameInput,
            scope=ScopeEnum.SINGLETON)

    def __init__(self):
        self._ioc = StaticContainerBuilder()
        self._bindings = {}
