from pygame import Vector2

from .component_base import ComponentBase
from ..lib import RepeatingAnimation, NullAnimation
from ..enum import StateEnum, GameObjectMessageEnum
from ..typing import IBehaviorComponent, IWorldMap
from ..models import AnimationSpec
from ..mixins import AssetMixin


class AnimatedSprite(ComponentBase, AssetMixin, IBehaviorComponent):

    subscriptions = [
        GameObjectMessageEnum.STATE_CHANGED,
        GameObjectMessageEnum.SET_ANIMATION
    ]

    def update(self, frame_delta: float, world: IWorldMap) -> None:
        self.animation.update(frame_delta)
        self.set_state(StateEnum.SPRITE, self.animation.sprite)
        self._run_tasks()

    def on_set_animation(self, sender: object, value: str):
        if self.animation.name != value:
            self._set_animation(value)

    def on_state_changed(self, sender: object, key: StateEnum):
        if key != StateEnum.WORLD_LOCATION:
            return
        self._defer_task(self._adjust_location)

    def _adjust_location(self):

        # Collect the values
        footprint = self.animation.footprint
        bounding_box = self.animation.bounding_box

        # Compute bbox relative position to footprint
        bb_x_offset = footprint.x - bounding_box.x
        bb_y_offset = footprint.y - bounding_box.y

        # Compute footprint relative position to zero
        fp_x_offset = 0 - footprint.x
        fp_y_offset = 0 - footprint.y

        # Move footprint's center to world location
        footprint.center = self.get_state(StateEnum.WORLD_LOCATION)

        # adjust bounding box position using offset from footprint
        bounding_box.x = footprint.x - bb_x_offset
        bounding_box.y = footprint.y - bb_y_offset

        # Compute topleft corner of sprite
        sprite_location = footprint.x + fp_x_offset, footprint.y + fp_y_offset

        # Publish the values
        self.parent.set_state(StateEnum.FOOTPRINT, footprint)
        self.parent.set_state(StateEnum.BOUNDING_BOX, bounding_box)
        self.parent.set_state(StateEnum.SPRITE_LOCATION, sprite_location)

    def _defer_task(self, task):
        self._tasks.add(task)

    def _run_tasks(self):
        for task in self._tasks:
            task()
        self._tasks = set()

    def _set_animation(self, value):
        # TODO: This needs to select the correct animation type (repeating or not-repeating)
        self.animation = RepeatingAnimation(self._animation_specs[value], self._sprite_sheets)
        self._defer_task(self._adjust_location)

    def __init__(self, *animation_map, **defaults):
        self._animation_specs = {}
        self._tasks = set()

        sheets_to_load = set()
        for raw in animation_map:
            spec = AnimationSpec.parse(raw, **defaults)
            self._animation_specs[spec.name] = spec
            for frame in spec.frames:
                sheets_to_load.add(frame.sprite_sheet)

        self._sprite_sheets = {
            sheet: self.asset_manager.get_sprite_sheet(sheet)
            for sheet in sheets_to_load
        }

        self.animation = NullAnimation()
