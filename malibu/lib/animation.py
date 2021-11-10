from pygame import Rect, Surface
from typing import List, Dict

from ..models import AnimationSpec
from ..typing import IAnimation


class NullAnimation(IAnimation):

    @property
    def complete(self) -> bool: return True

    @property
    def name(self) -> str: return ""

    @property
    def sprite(self) -> Surface: return self._surface

    @property
    def bounding_box(self) -> Rect: return self._bb

    @property
    def footprint(self) -> Rect: return self._fp

    def update(self, frame_delta: float): pass

    def __init__(self):
        self._surface = Surface((0, 0))
        self._bb = Rect(0, 0, 0, 0)
        self._fp = self._bb.copy()


class RepeatingAnimation(IAnimation):

    @property
    def complete(self) -> bool:
        return False

    @property
    def name(self) -> str:
        return self._name

    @property
    def sprite(self) -> Surface:
        frame = self._get_current_frame()
        return self._sheets[frame.sprite_sheet][frame.index]

    @property
    def bounding_box(self) -> Rect:
        frame = self._get_current_frame()
        return Rect(frame.bounding_box)

    @property
    def footprint(self) -> Rect:
        frame = self._get_current_frame()
        return Rect(frame.footprint)

    def update(self, frame_delta: float):
        self._duration += (frame_delta * 1000)
        frame = self._get_current_frame()
        if self._duration >= frame.frame_delay:
            self._frame_index = (self._frame_index + 1) % len(self._frames)
            self._duration -= frame.frame_delay

    def _get_current_frame(self):
        return self._frames[self._frame_index]

    def __init__(self, spec: AnimationSpec, sheet_map: Dict[str, List[Surface]]):
        self._name = spec.name
        self._sheets = sheet_map
        self._frames = spec.frames
        self._frame_index = 0
        self._duration = 0
