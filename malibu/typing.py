from pygame import Vector2, Surface, Rect
from pygame.event import Event
from abc import ABC, abstractmethod
from typing import Set, Iterable, Optional, Union, Generator, List

from .models import AudioSpec, MapSpec
from .enum import (
    AudioEdgeTransitionEnum,
    SceneEnum,
    SpriteEnum,
    ComponentMessageEnum,
    MaterialEnum,
)


class IAudioService(ABC):
    @abstractmethod
    def set_music(self, name: Union[str, None], edge_transition: Optional[AudioEdgeTransitionEnum] = None) -> None: ...
    @abstractmethod
    def enqueue(self, name: str, point: Vector2) -> None: ...
    @abstractmethod
    def update(self, origin: Vector2) -> None: ...


class IKeyboardService(ABC):
    @abstractmethod
    def is_pressed(self, key: int) -> bool: ...
    @abstractmethod
    def is_released(self, key: int) -> bool: ...
    @abstractmethod
    def is_held(self, key: int) -> bool: ...
    @abstractmethod
    def get_pressed(self) -> Set[int]: ...
    @abstractmethod
    def get_released(self) -> Set[int]: ...
    @abstractmethod
    def get_held(self) -> Set[int]: ...
    @abstractmethod
    def update(self, events: Iterable[Event]) -> None: ...


class IAssetService(ABC):
    @abstractmethod
    def get_audio_spec(self, name: str) -> AudioSpec: ...
    @abstractmethod
    def iter_audio_specs(self) -> Generator[AudioSpec, None, None]: ...
    @abstractmethod
    def get_map_spec(self, name: str) -> MapSpec: ...


class ISettingsService(ABC):
    ...


class ISceneFactoryService(ABC):
    @abstractmethod
    def new(self, scene: SceneEnum) -> "IGameScene": ...


class ISpriteFactoryService(ABC):
    @abstractmethod
    def new(self, sprite_name: SpriteEnum) -> "IGameSprite": ...


class IGameScene(ABC):
    @abstractmethod
    def activate(self) -> None: ...
    @abstractmethod
    def inactivate(self) -> None: ...
    @abstractmethod
    def process_inputs(self) -> None: ...
    @abstractmethod
    def update(self, frame_delta: float) -> None: ...
    @abstractmethod
    def render(self) -> None: ...


class IGameService(ABC):
    @abstractmethod
    def run(self, scene: IGameScene) -> None: ...
    @abstractmethod
    def close(self) -> None: ...
    @abstractmethod
    def set_scene(self, scene: IGameScene) -> None: ...


class INotifiableComponent(ABC):
    @abstractmethod
    def notify(self, sender: object, msg_type: ComponentMessageEnum, value: any): ...


class INotifierGameSprite(ABC):
    @abstractmethod
    def subscribe(self, msg_type: ComponentMessageEnum, component: INotifiableComponent): ...
    @abstractmethod
    def broadcast(self, sender: object, msg_type: ComponentMessageEnum, value: any): ...


class IGameSpriteComponent(ABC):
    @abstractmethod
    def set_container(self, sprite: INotifierGameSprite): ...


class IGameSpriteInputComponent(IGameSpriteComponent):
    @abstractmethod
    def process_input(self, keyboard: IKeyboardService): ...


class IGameSpritePhysicsComponent(IGameSpriteComponent):
    @abstractmethod
    def update(self, frame_delta: float, tile_map: "ITileMap"): ...


class IGameSpriteGraphicsComponent(IGameSpriteComponent):
    @abstractmethod
    def render(self, gfx: Surface): ...


class IGameSprite(ABC):
    @property
    @abstractmethod
    def input_component(self) -> IGameSpriteInputComponent: ...
    @input_component.setter
    @abstractmethod
    def input_component(self, val: IGameSpriteInputComponent) -> None: ...
    @property
    @abstractmethod
    def physics_component(self) -> IGameSpritePhysicsComponent: ...
    @physics_component.setter
    @abstractmethod
    def physics_component(self, val: IGameSpritePhysicsComponent) -> None: ...
    @property
    @abstractmethod
    def graphics_component(self) -> IGameSpriteGraphicsComponent: ...
    @graphics_component.setter
    @abstractmethod
    def graphics_component(self, val: IGameSpriteGraphicsComponent) -> None: ...


class ITileMap(ABC):
    @abstractmethod
    def render(self, gfx: Surface) -> None: ...
    @abstractmethod
    def update(self, frame_delta: float) -> None: ...
    @abstractmethod
    def is_walkable(self, rect: Rect) -> bool: ...
    @abstractmethod
    def get_material(self, rect: Rect) -> MaterialEnum: ...
    @abstractmethod
    def get_sprites(self) -> List[IGameSprite]: ...
    @abstractmethod
    def get_default_music(self) -> str: ...


class IMapFactoryService(ABC):
    @abstractmethod
    def get_tile_map(self, name: str) -> ITileMap: ...
