from pygame import Vector2
from pygame.mixer import Sound, Channel, set_num_channels, set_reserved
from typing import List, Optional, Tuple, Dict, Union

from .locator import ServiceLocator

from ..typing import IAudioService, IGameObject
from ..enum import AudioTypeEnum, AudioEdgeTransitionEnum, GameObjectMessageEnum
from ..models import AudioSpec
from ..mixins import LoggerMixin, AssetMixin


class AudioService(LoggerMixin, AssetMixin, IAudioService):

    focus_point: Vector2 = Vector2(0)
    cross_fade_ms = 2000

    def initialize(self):
        set_num_channels(100)
        set_reserved(0)
        set_reserved(1)
        self._music_channel = Channel(0)
        self._next_music_channel = Channel(1)
        self._sounds = {spec.name: Sound(spec.path) for spec in self.asset_manager.iter_audio_specs()}
        self._set_focus(ServiceLocator.get_graphics().get_viewport().center)

    def attach(self, obj: IGameObject) -> None:
        obj.subscribe(GameObjectMessageEnum.SET_LOCATION, self)

    def detach(self, obj: IGameObject) -> None:
        obj.unsubscribe(GameObjectMessageEnum.SET_LOCATION, self)
        self._set_focus(ServiceLocator.get_graphics().get_viewport().center)

    def receive_message(self, sender: object, msg_type: GameObjectMessageEnum, value: any):
        self._set_focus(value)

    def set_music(self, name: Union[str, None], edge_transition: Optional[AudioEdgeTransitionEnum] = None) -> None:
        edge_transition = edge_transition or AudioEdgeTransitionEnum.CROSSFADE
        spec = self.asset_manager.get_audio_spec(name)
        sound = self._get_sound(spec)

        if self._current_music == sound:
            return
        self._current_music = sound
        self.log.info("Begin playing music: %s", spec)

        self._next_music_channel.set_volume(spec.gain)
        if edge_transition == AudioEdgeTransitionEnum.CROSSFADE:
            self._next_music_channel.play(sound, loops=-1, fade_ms=self.cross_fade_ms)
            self._music_channel.fadeout(self.cross_fade_ms)
        elif edge_transition == AudioEdgeTransitionEnum.FADEIN:
            self._next_music_channel.play(sound, loops=-1, fade_ms=self.cross_fade_ms)
            self._music_channel.stop()
        elif edge_transition == AudioEdgeTransitionEnum.FADEOUT:
            self._next_music_channel.play(sound, loops=-1)
            self._music_channel.fadeout(self.cross_fade_ms)
        elif edge_transition == AudioEdgeTransitionEnum.NONE:
            self._next_music_channel.play(sound, loops=-1)
            self._music_channel.stop()

        # swap the channels for the next play
        temp: Channel = self._music_channel
        self._music_channel = self._next_music_channel
        self._next_music_channel = temp

    def enqueue(self, name: str, point: Vector2) -> None:
        spec = self.asset_manager.get_audio_spec(name)
        if spec is not None:
            self._buffer.append((spec, point))
        else:
            self.log.critical("Dropping request for unknown audio spec: %s.", name)

    def update(self) -> None:
        todo: Dict[AudioTypeEnum, Dict[str, Tuple[AudioSpec, float]]] = {
            AudioTypeEnum.KINETIC: {},
            AudioTypeEnum.PASSIVE: {},
        }

        # Deduplicate and sort enqueued requests
        for spec, point in self._buffer:
            volume = self._compute_volume(spec, self.focus_point, point)
            if volume <= 0:
                # Drop audio that will not be heard
                continue
            if spec.name in todo[spec.type]:
                _, other_volume = todo[spec.type][spec.name]
                volume = max(volume, other_volume)
            todo[spec.type][spec.name] = (spec, volume)

        # Update the passive audio volume and start any new passive audio
        for spec, volume in todo[AudioTypeEnum.PASSIVE].values():
            sound = self._get_sound(spec)
            sound.set_volume(volume)
            if spec.name not in self._playing:
                self.log.debug("Playing passive sound: %s", spec)
                self._playing[spec.name] = sound
                sound.play(loops=-1)

        # Stop any passive audio that was not included
        for name in self._playing - todo[AudioTypeEnum.PASSIVE].keys():
            self.log.debug("Stopping passive sound: %s", name)
            self._playing[name].fadeout(100)
            del self._playing[name]

        # Play kinetic audio
        for spec, volume in todo[AudioTypeEnum.KINETIC].values():
            self.log.debug("Playing kinetic sound: %s", spec)
            sound = self._get_sound(spec)
            sound.set_volume(volume)
            sound.play()

        self._buffer = list()

    def _set_focus(self, point):
        x, y, *_ = point
        self.focus_point = Vector2(x, y)

    def _get_sound(self, spec: AudioSpec) -> Sound:
        """Obtain a sound that can be played.

        Kinetic sounds will be cloned before returning. All other sounds
        will return the root sound object for the given specification.
        """
        if spec.name not in self._sounds:
            self.log.warning("Sound file not loaded. Fetching from disk: %s", spec)
            self._sounds[spec.name] = Sound(spec.path)
        sound = self._sounds[spec.name]
        if spec.type == AudioTypeEnum.KINETIC:
            return Sound(sound)
        else:
            return sound

    def _compute_volume(self, spec: AudioSpec, origin: Vector2, point: Vector2) -> float:
        """Compute the volume for sound given a distance as 2 points"""
        volume = ((spec.distance - origin.distance_to(point)) / spec.distance) * spec.gain
        return volume if volume > 0 else 0

    def __init__(self):
        self._buffer: List[Tuple[AudioSpec, Vector2]] = list()
        self._playing: Dict[str, Sound] = {}
        self._music_channel: Optional[Channel] = None
        self._next_music_channel: Optional[Channel] = None
        self._sounds: Dict[str, Sound] = {}
        self._current_music: Optional[Sound] = None
