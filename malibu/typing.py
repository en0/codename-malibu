from pygame import Vector2, Surface, Rect
from pygame.event import Event
from abc import ABC, abstractmethod
from typing import Set, Iterable, Optional, Union, Generator, List, Tuple, Type, TypeVar

from .models import AudioSpec, MapSpec
from .enum import (
    AudioEdgeTransitionEnum,
    SceneEnum,
    GameObjectEnum,
    ComponentMessageEnum,
    MaterialEnum,
)


T_GameComponent = TypeVar("T_GameComponent", bound="IGameComponent")


class IAttachable(ABC):
    @abstractmethod
    def attach(self, obj: "IGameObject") -> None: ...
    @abstractmethod
    def detach(self, obj: "IGameObject") -> None: ...


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


class ISceneFactory(ABC):
    @abstractmethod
    def new(self, scene: SceneEnum) -> "IGameScene": ...


class IObjectFactory(ABC):
    @abstractmethod
    def new(self, sprite_name: GameObjectEnum) -> "IGameObject": ...


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
    @abstractmethod
    def push_scene(self, scene: IGameScene) -> None: ...
    @abstractmethod
    def pop_scene(self) -> IGameScene: ...
    @abstractmethod
    def get_current_scene(self) -> IGameScene: ...


class INotifiableObject(ABC):
    @abstractmethod
    def receive_message(self, sender: object, msg_type: ComponentMessageEnum, value: any): ...


class IGameComponent(INotifiableObject):
    @abstractmethod
    def set_parent(self, game_object: "IGameObject"): ...


class IInputComponent(IGameComponent):
    @abstractmethod
    def process_input(self, keyboard: IKeyboardService): ...


class IPhysicsComponent(IGameComponent):
    @abstractmethod
    def update(self, frame_delta: float, world: "IWorldMap"): ...


class IGraphicsComponent(IGameComponent):
    @abstractmethod
    def render(self, gfx: Surface): ...


class IGameObject(INotifiableObject):
    @abstractmethod
    def process_input(self, keyboard: IKeyboardService): ...
    @abstractmethod
    def update(self, frame_delta: float, world: "IWorldMap"): ...
    @abstractmethod
    def render(self, gfx: Surface): ...
    @abstractmethod
    def subscribe(self, msg_type: ComponentMessageEnum, component: INotifiableObject): ...
    @abstractmethod
    def unsubscribe(self, msg_type: ComponentMessageEnum, component: INotifiableObject): ...
    @abstractmethod
    def get_component(self, component_type: Type[T_GameComponent]) -> Optional[T_GameComponent]: ...


class IWorldMap(ABC):
    @abstractmethod
    def render(self, gfx: Surface, rect: Rect) -> None: ...
    @abstractmethod
    def update(self, frame_delta: float) -> None: ...
    @abstractmethod
    def is_walkable(self, rect: Rect) -> bool: ...
    @abstractmethod
    def get_material(self, rect: Rect) -> MaterialEnum: ...
    @abstractmethod
    def get_sprites(self) -> List[IGameObject]: ...
    @abstractmethod
    def get_default_music(self) -> str: ...
    @abstractmethod
    def get_rect(self) -> Rect: ...


class IWorldFactory(ABC):
    @abstractmethod
    def build_world(self, name: str) -> IWorldMap: ...


class ICamera(INotifiableObject, IAttachable):
    @property
    @abstractmethod
    def world_offset(self): ...
    @property
    @abstractmethod
    def aperture(self) -> Rect: ...
    @abstractmethod
    def set_world_rect(self, rect: Rect) -> None: ...
    @abstractmethod
    def receive_message(self, sender: object, msg_type: ComponentMessageEnum, value: any): ...

class IAudioService(INotifiableObject, IAttachable):
    @abstractmethod
    def set_music(self, name: Union[str, None], edge_transition: Optional[AudioEdgeTransitionEnum] = None) -> None: ...
    @abstractmethod
    def enqueue(self, name: str, point: Vector2) -> None: ...
    @abstractmethod
    def update(self, origin: Vector2) -> None: ...
