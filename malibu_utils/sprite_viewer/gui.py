import pygame
import pygame_gui
from typing import Tuple


def _rect(x=0, y=0, w=100, h=35):
    return pygame.Rect(x, y, w, h)


def _below(elem, pad, w=None, h=None):
    a: pygame.Rect = elem.relative_rect.copy()
    a.width = w or elem.relative_rect.width
    a.height = h or elem.relative_rect.height
    a.top = elem.relative_rect.bottom + pad
    return a


def _left_of(elem, pad, w=None, h=None):
    a: pygame.Rect = elem.relative_rect.copy()
    a.width = w or elem.relative_rect.width
    a.height = h or elem.relative_rect.height
    a.left = elem.relative_rect.right + pad
    return a


def _right_top_in(elem, pad, w, h):
    x = elem.rect.width - w - pad
    return pygame.Rect(x, pad, w, h)


def _left_top_in(elem, pad, w, h):
    return pygame.Rect(pad, pad, w, h)


def _left_bottom_in(elem, pad, w, h):
    y = elem.rect.height - h - pad
    return pygame.Rect(pad, y, w, h)


class _HandlingUIManager(pygame_gui.UIManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._listeners = {}

    def on(self, event, elem, fn):
        self._listeners[(elem, event)] = fn

    def process_events(self, event):
        super().process_events(event)
        if event.type == pygame.USEREVENT and hasattr(event, "ui_element"):
            k = (event.ui_element, event.user_type)
            fn = self._listeners.get(k)
            if fn: fn(event)


class SpriteViewUI(_HandlingUIManager):

    def show_speed(self, speed: str):
        self.lbl_speed.set_text(f"Animation Speed: {speed}")

    def show_zoom(self, zoom: str):
        self.lbl_zoom.set_text(f"Animation zoom: {zoom}")

    def update_animation_details(self, spec, frame):
        if spec is None and self.current_spec is not None:
            self.current_spec = None
            self.current_frame_spec = None
            self.lbl_anim_details = pygame_gui.elements.UITextBox(
                "<b>Animation Details</b><br><i>Select Animation</i>",
                _left_of(self.btn_reset, 0, h=155, w=310),
                manager=self)
            self.lbl_frame_details = pygame_gui.elements.UITextBox(
                "<b>Frame Details</b><br><i>Select Animation</i>",
                _left_of(self.lbl_anim_details, 0),
                manager=self)
        if spec is None:
            return

        if self.current_spec != spec:
            self.current_spec = spec
            self.lbl_anim_details = pygame_gui.elements.UITextBox(
                f"<p><b>Animation:</b> {spec.name}</p><br />"
                f"<p><b>Repeat:</b> {spec.repeat}</p>",
                _left_of(self.btn_reset, 0, h=155, w=310),
                manager=self)

        if self.current_frame_spec != spec.frames[frame]:
            self.current_frame_spec = spec.frames[frame]
            f = spec.frames[frame]
            self.lbl_frame_details = pygame_gui.elements.UITextBox(
                f"<b>Frame:</b> {f.sheet}[{f.index}]<br/>"
                f"<b>Delay:</b> {f.delay}<br/>"
                f"<b>Mirrored:</b> {f.mirror}<br/>"
                f"<b>Fipped:</b> {f.flip}<br/>"
                f"<b>Opacity:</b> {f.opacity}<br/>"
                f"<b>Rotation:</b> {f.rotation}<br/>"
                f"<b>Scale:</b> {f.scale_width}, {f.scale_height}<br/>",
                _left_of(self.lbl_anim_details, 0),
                manager=self)

    def add_base_animation_name(self, name: str):
        self._base_anims.append(name)

    def add_trigger_animation_name(self, name: str):
        self._trigger_anims.append(name)

    def on_reset(self, cb):
        self._on_reset = cb

    def on_trigger(self, cb):
        self._on_trigger = cb

    def on_pause(self, cb):
        self._on_pause = cb

    def on_resume(self, cb):
        self._on_resume = cb

    def on_speed_increase(self, cb):
        self._on_speed_increase = cb

    def on_speed_decrease(self, cb):
        self._on_speed_decrease = cb

    def on_zoom_in(self, cb):
        self._on_zoom_in = cb

    def on_zoom_out(self, cb):
        self._on_zoom_out = cb

    def on_zoom_reset(self, cb):
        self._on_zoom_reset = cb

    def on_base_animation_changed(self, cb):
        self._on_base_animation_changed = cb

    def on_trigger_animation_changed(self, cb):
        self._on_trigger_animation_changed = cb

    def _dispatch(self, handler, *args):
        if handler is not None:
            handler(*args)

    def _toggle_freeze(self):
        if self._is_paused:
            self.btn_freeze.set_text("Pause")
            self._is_paused = False
            self._dispatch(self._on_resume)
        else:
            self.btn_freeze.set_text("Resume")
            self._is_paused = True
            self._dispatch(self._on_pause)

    def __init__(self, window_resolution: Tuple[int, int]):
        super().__init__(window_resolution)
        self._base_anims = ["Select Base Animation"]
        self._trigger_anims = ["Select Trigger Animation"]
        self.rect = pygame.Rect(0, 0, *window_resolution)

        self.current_spec = None
        self.current_frame_spec = None

        self._is_paused = False
        self._on_base_animation_changed = None
        self._on_trigger_animation_changed = None
        self._on_reset = None
        self._on_trigger = None
        self._on_speed_increase = None
        self._on_speed_decrease = None
        self._on_pause = None
        self._on_resume = None
        self._on_zoom_in = None
        self._on_zoom_out = None
        self._on_zoom_reset = None

        # UI Elements

        pnl_bottom = pygame_gui.elements.UIPanel(
            _left_top_in(self, 0, self.rect.width, 180),
            0,
            self)

        self.ddl_base_animation = pygame_gui.elements.UIDropDownMenu(
            self._base_anims, self._base_anims[0],
            _left_top_in(self, 10, w=300, h=35),
            manager=self)

        self.ddl_trigger_animation = pygame_gui.elements.UIDropDownMenu(
            self._trigger_anims, self._trigger_anims[0],
            _below(self.ddl_base_animation, 5),
            manager=self)

        self.btn_reset = pygame_gui.elements.UIButton(
            _left_of(self.ddl_base_animation, 5, w=80),
            "Reset",
            manager=self)

        self.btn_trigger = pygame_gui.elements.UIButton(
            _left_of(self.ddl_trigger_animation, 5, w=80),
            "Trigger",
            manager=self)

        self.lbl_speed = pygame_gui.elements.UILabel(
            _below(self.ddl_trigger_animation, 5, w=230),
            f"Animtion Speed: ...",
            manager=self)

        self.btn_slow_down = pygame_gui.elements.UIButton(
            _left_of(self.lbl_speed, 5, w=30),
            "-",
            manager=self)

        self.btn_speed_up = pygame_gui.elements.UIButton(
            _left_of(self.btn_slow_down, 5, w=30),
            "+",
            manager=self)

        self.btn_freeze = pygame_gui.elements.UIButton(
            _left_of(self.btn_speed_up, 5, w=80),
            "Pause",
            manager=self)

        self.lbl_zoom = pygame_gui.elements.UILabel(
            _below(self.lbl_speed, 5, w=230),
            f"Animation Zoom: ...",
            manager=self)

        self.btn_zoom_out = pygame_gui.elements.UIButton(
            _left_of(self.lbl_zoom, 5, w=30),
            "-",
            manager=self)

        self.btn_zoom_in = pygame_gui.elements.UIButton(
            _left_of(self.btn_zoom_out, 5, w=30),
            "+",
            manager=self)

        self.btn_zoom_reset = pygame_gui.elements.UIButton(
            _left_of(self.btn_zoom_in, 5, w=80),
            "Reset",
            manager=self)

        self.lbl_anim_details = pygame_gui.elements.UITextBox(
            "<b>Animation Details</b><br><i>Select Animation</i>",
            _left_of(self.btn_reset, 0, h=155, w=310),
            manager=self)

        self.lbl_frame_details = pygame_gui.elements.UITextBox(
            "<b>Frame Details</b><br><i>Select Animation</i>",
            _left_of(self.lbl_anim_details, 0),
            manager=self)

        self.frame_area_rect = pygame.Rect(
            0, pnl_bottom.rect.bottom, self.rect.width,
            self.rect.height - pnl_bottom.rect.height)

        # Event Handlers

        self.on(
            event=pygame_gui.UI_BUTTON_PRESSED,
            elem=self.btn_reset,
            fn=lambda x: self._dispatch(self._on_reset))

        self.on(
            event=pygame_gui.UI_BUTTON_PRESSED,
            elem=self.btn_trigger,
            fn=lambda x: self._dispatch(self._on_trigger))

        self.on(
            event=pygame_gui.UI_BUTTON_PRESSED,
            elem=self.btn_speed_up,
            fn=lambda x: self._dispatch(self._on_speed_increase))

        self.on(
            event=pygame_gui.UI_BUTTON_PRESSED,
            elem=self.btn_slow_down,
            fn=lambda x: self._dispatch(self._on_speed_decrease))

        self.on(
            event=pygame_gui.UI_BUTTON_PRESSED,
            elem=self.btn_freeze,
            fn=lambda x: self._dispatch(self._toggle_freeze))

        self.on(
            event=pygame_gui.UI_BUTTON_PRESSED,
            elem=self.btn_zoom_in,
            fn=lambda x: self._dispatch(self._on_zoom_in))

        self.on(
            event=pygame_gui.UI_BUTTON_PRESSED,
            elem=self.btn_zoom_out,
            fn=lambda x: self._dispatch(self._on_zoom_out))

        self.on(
            event=pygame_gui.UI_BUTTON_PRESSED,
            elem=self.btn_zoom_reset,
            fn=lambda x: self._dispatch(self._on_zoom_reset))

        self.on(
            event=pygame_gui.UI_DROP_DOWN_MENU_CHANGED,
            elem=self.ddl_base_animation,
            fn=lambda x: self._dispatch(
                self._on_base_animation_changed,
                self.ddl_base_animation.selected_option))

        self.on(
            event=pygame_gui.UI_DROP_DOWN_MENU_CHANGED,
            elem=self.ddl_trigger_animation,
            fn=lambda x: self._dispatch(
                self._on_trigger_animation_changed,
                self.ddl_trigger_animation.selected_option))
