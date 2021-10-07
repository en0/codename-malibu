from pygame import Surface, transform, Rect
from typing import List, Callable
from logging import getLogger

from .typing import IAnimation, IAssetManager
from .model import AnimationSpec, AnimationFrameSpec


_log = getLogger(__name__)
UpdateMethodFn = Callable[["BasicAnimation", float], None]


class BasicAnimation(IAnimation):

    @property
    def name(self) -> str:
        return self._name

    @property
    def complete(self) -> bool:
        return self._complete

    @property
    def image(self) -> Surface:
        return self._tiles[self._frame_index]

    @property
    def current_frame_index(self):
        return self._frame_index

    def reset(self) -> None:
        _log.debug(f"Resetting animation: %s", self.name)
        self._complete = False
        self._update_method = self._init_update_method
        self._repeat_count = self._init_repeat_count
        self._frame_duration = 0
        self._frame_index = 0

    def get_footprint(self) -> Rect:
        return self._footprints[self._frame_index].copy()

    def get_boundary(self) -> Rect:
        return self._boundaries[self._frame_index].copy()

    def update(self, frame_delta: int) -> None:
        self._update_method(frame_delta / 1000.0)

    def has_flag(self, flag_name: str) -> bool:
        return flag_name in self._flags

    def _update_noop(self, frame_delay) -> None:
        pass

    def _update_repeat_and_stop(self, frame_delta) -> None:
        self._frame_duration += frame_delta
        if self._frame_duration < self._frame_delay:
            return

        # Compute next frame

        # If we are on the last frame, our behavior might change.
        on_last_frame = self._frame_index == len(self._tiles) - 1
        self._frame_duration = 0

        if on_last_frame and self._repeat_count > 0:
            # There is a repeat count. We need to run the animation again
            self._repeat_count -= 1
            self._frame_index = 0
        elif on_last_frame and self._repeat_count == 0:
            # There are no repeats left. animation becomes staic.
            self._update_method = self._update_noop
            self._complete = True
        else:
            # Next Frame
            self._frame_index += 1

    def _update_repeat_forever(self, frame_delta) -> None:
        self._frame_duration += frame_delta
        if self._frame_duration < self._frame_delay:
            return

        # Next Frame
        self._frame_duration = 0
        self._frame_index = (self._frame_index + 1) % len(self._tiles)

    @property
    def _frame_delay(self) -> float:
        return self._deltas[self._frame_index]

    def __init__(self, spec: AnimationSpec, asset_manager: IAssetManager):

        _log.info(f"Loading animation: %s", spec.name)

        self._spec = spec
        self._name = spec.name
        self._tiles: List[Surface] = []
        self._deltas: List[float] = []
        self._boundaries: List[Rect] = []
        self._footprints: List[Rect] = []
        self._complete = False
        self._init_repeat_count = spec.repeat
        self._repeat_count = spec.repeat
        self._frame_duration: float = 0.0
        self._frame_index: int = 0
        self._flags = spec.flags.copy()
        self._update_method: UpdateMethodFn = None
        self._init_update_method: UpdateMethodFn = (
            self._update_noop if len(spec.frames) == 1 else
            self._update_repeat_forever if spec.repeat == -1 else
            self._update_repeat_and_stop
        )

        _log.debug(f"Using animation update method: %s", self._init_update_method)

        for i, frame in enumerate(spec.frames):
            _log.debug(f"Loading frame %s[%s]: %s", self._name, i, frame)
            tile = asset_manager.get_sprite_sheet_tile(frame.sheet, frame.index)
            if frame.flip or frame.mirror:
                tile = transform.flip(tile, frame.mirror, frame.flip)
            if frame.rotation != 0:
                tile = transform.rotate(tile, frame.rotation)
            if frame.opacity != 0:
                tile.set_alpha(frame.opacity)
            if frame.scale_width != 1.0 or frame.scale_height != 1.0:
                x, y = tile.get_size()
                scale_x = int(x * frame.scale_width)
                scale_y = int(x * frame.scale_height)
                tile = transform.scale(tile, (scale_x, scale_y))

            # Convert the delay to seconds
            self._deltas.append(frame.delay / 1000.0)
            self._tiles.append(tile)
            self._boundaries.append(frame.boundary)
            self._footprints.append(frame.footprint)

        self.reset()
