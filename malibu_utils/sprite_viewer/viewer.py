import pygame
import pkg_resources
from malibu_lib import BasicAnimation
from malibu_lib.typing import IAssetManager

from .gui import SpriteViewUI
from ..watcher.watch import FileWatcher


class SpriteViewer:

    @property
    def current_animation(self):
        if self.trigger_animation and self.trigger_animation.complete:
            self.target_animation = "base"
        elif self.trigger_animation is None:
            self.target_animation = "base"
        if self.target_animation == "base":
            return self.base_animation
        else:
            return self.trigger_animation

    @property
    def current_animation_spec(self):
        if self.trigger_animation and self.trigger_animation.complete:
            self.target_animation = "base"
        elif self.trigger_animation is None:
            self.target_animation = "base"
        if self.target_animation == "base":
            return self.base_animation_spec
        else:
            return self.trigger_animation_spec

    def update(self, frame_delta: float):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.ui.process_events(event)

        if self.current_animation and not self.freeze:
            adj = frame_delta * self.speed_adjust
            self.current_animation.update(frame_delta + adj)

        self.ui.update_animation_details(
            self.current_animation_spec,
            self.current_animation_spec and self.current_animation.current_frame_index)

        self.ui.update(frame_delta)

        if self.watcher.has_changed():
            self.reload_spec()

    def render(self):
        # Render frame and ui
        if self.current_animation:
            rect = self.current_animation.image.get_rect()
            rect.center = self.frame_rect.width // 2, self.frame_rect.height // 2
            self.frame.blit(self.current_animation.image, rect)

        _frame = pygame.transform.scale(self.frame, self.ui.frame_area_rect.size)
        self.display.blit(_frame, self.ui.frame_area_rect.topleft)
        self.ui.draw_ui(self.display)

        # present the buffer
        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            self.display.fill(self.bg_color)
            self.frame.fill(self.bg_color)
            frame_delta = self.clock.tick(60)
            self.update(frame_delta)
            self.render()

    def reset_base_animation(self):
        if self.base_animation:
            self.base_animation.reset()

    def trigger_overlay_animation(self):
        if self.trigger_animation:
            self.target_animation = "trigger"
            self.trigger_animation.reset()

    def adjust_speed(self, delta):
        self.speed_adjust += delta
        if self.speed_adjust > 1:
            self.speed_adjust = 1
        elif self.speed_adjust < -1:
            self.speed_adjust = -1
        self.ui.show_speed(f"{int((self.speed_adjust + 1) * 100)}%")

    def adjust_zoom(self, delta):
        self._scale_factor += delta
        if self._scale_factor > 1:
            self._scale_factor = 1.0
        elif self._scale_factor < 0.1:
            self._scale_factor = 0.1
        self.ui.show_zoom(f"{100 - int((self._scale_factor - 0.1) / 0.9 * 100)}%")
        w, h = self.ui.frame_area_rect.size
        w = int(w * self._scale_factor)
        h = int(h * self._scale_factor)
        self.frame_rect = pygame.Rect(0, 0, w, h)
        self.frame = pygame.Surface(self.frame_rect.size)

    def set_pause(self, state):
        self.freeze = state

    def load_base_animation(self, name: str):
        if name in self.spec.animations:
            self.base_animation_spec = self.spec.animations[name]
            self.base_animation = BasicAnimation(self.base_animation_spec, self.am)
        else:
            self.base_animation_spec = None
            self.base_animation = None

    def load_trigger_animation(self, name: str):
        if name in self.spec.animations:
            self.trigger_animation_spec = self.spec.animations[name]
            self.trigger_animation = BasicAnimation(self.trigger_animation_spec, self.am)
        else:
            self.trigger_animation_spec = None
            self.trigger_animation = None

    def reload_spec(self):
        sprite_name = self.spec.name
        base_anim_name = self.base_animation_spec and self.base_animation_spec.name
        trigger_anim_name = self.trigger_animation_spec and self.trigger_animation_spec.name
        self.am.clear()
        self.spec = self.am.get_sprite_spec(sprite_name)
        self.load_base_animation(base_anim_name)
        self.load_trigger_animation(trigger_anim_name)

    def __init__(self, sprite_name: str, asset_manager: IAssetManager, display_size=(1024, 600), disp_opts=None):
        disp_opts = disp_opts or (
            pygame.HWACCEL |
            pygame.DOUBLEBUF
        )
        self.am = asset_manager
        self.spec = asset_manager.get_sprite_spec(sprite_name)
        self.bg_color = pygame.Color("#000000")
        self.clock_divider = 1.0
        self.running = False
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode(display_size, disp_opts)
        pygame.display.set_caption(f"Sprite Viewer: {sprite_name}")
        self.display_rect = self.display.get_rect()
        self.ui = SpriteViewUI(display_size)
        self.watcher = FileWatcher(self.am.get_sprite_spec_path(sprite_name))
        self.frame = pygame.Surface((self.ui.frame_area_rect.width, self.ui.frame_area_rect.height))
        self.frame_rect = self.frame.get_rect()

        self.base_animation = None
        self.base_animation_spec = None
        self.trigger_animation = None
        self.trigger_animation_spec = None
        self.speed_adjust = 0
        self._scale_factor = 0
        self.freeze = False
        self.target_animation = "base"

        # Load all the animations by name
        for spec in self.spec.animations:
            self.ui.add_base_animation_name(spec)
            self.ui.add_trigger_animation_name(spec)

        # Wire-up event handlers
        self.ui.on_reset(self.reset_base_animation)
        self.ui.on_trigger(self.trigger_overlay_animation)
        self.ui.on_base_animation_changed(self.load_base_animation)
        self.ui.on_trigger_animation_changed(self.load_trigger_animation)
        self.ui.on_speed_increase(lambda: self.adjust_speed(0.1))
        self.ui.on_speed_decrease(lambda: self.adjust_speed(-0.1))
        self.ui.on_pause(lambda: self.set_pause(True))
        self.ui.on_resume(lambda: self.set_pause(False))
        self.ui.on_zoom_in(lambda: self.adjust_zoom(-0.1))
        self.ui.on_zoom_out(lambda: self.adjust_zoom(0.1))
        self.ui.on_zoom_reset(lambda: self.adjust_zoom(-100))

        # Set default UI elements
        self.adjust_speed(0)
        self.adjust_zoom(-100)
