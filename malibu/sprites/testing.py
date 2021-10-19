import pygame

from ..enum import ComponentMessageEnum
from ..typing import (
    IGameSpriteGraphicsComponent,
    IGameSpriteInputComponent,
    IGameSpritePhysicsComponent,
    IKeyboardService,
    INotifiableComponent,
    INotifierGameSprite, ITileMap,
)


class TestInputComponent(IGameSpriteInputComponent):

    _container: INotifierGameSprite

    def process_input(self, keyboard: IKeyboardService):
        if keyboard.is_pressed(pygame.K_a):
            self._container.broadcast(self, ComponentMessageEnum.SET_VELOCITY, pygame.Vector2(-1, 0))
        elif keyboard.is_pressed(pygame.K_d):
            self._container.broadcast(self, ComponentMessageEnum.SET_VELOCITY, pygame.Vector2(1, 0))
        elif keyboard.is_pressed(pygame.K_w):
            self._container.broadcast(self, ComponentMessageEnum.SET_VELOCITY, pygame.Vector2(0, -1))
        elif keyboard.is_pressed(pygame.K_s):
            self._container.broadcast(self, ComponentMessageEnum.SET_VELOCITY, pygame.Vector2(0, 1))
        elif keyboard.is_released(pygame.K_a):
            self._container.broadcast(self, ComponentMessageEnum.SET_VELOCITY, pygame.Vector2(0, 0))
        elif keyboard.is_released(pygame.K_d):
            self._container.broadcast(self, ComponentMessageEnum.SET_VELOCITY, pygame.Vector2(0, 0))
        elif keyboard.is_released(pygame.K_w):
            self._container.broadcast(self, ComponentMessageEnum.SET_VELOCITY, pygame.Vector2(0, 0))
        elif keyboard.is_released(pygame.K_s):
            self._container.broadcast(self, ComponentMessageEnum.SET_VELOCITY, pygame.Vector2(0, 0))

    def set_container(self, sprite: INotifierGameSprite):
        self._container = sprite


class TestPhysicsComponent(IGameSpritePhysicsComponent, INotifiableComponent):

    _material: str = ""
    _container: INotifierGameSprite
    _pos = pygame.Vector2(100, 100)
    _velocity: pygame.Vector2 = pygame.Vector2(0, 0)
    _move_speed = 100

    def notify(self, sender: object, msg_type: ComponentMessageEnum, value: any):
        self._velocity = value

    def update(self, frame_delay: float, tile_map: ITileMap):
        if self._velocity.x == 0 and self._velocity.y == 0:
            return
        new_pos = self._velocity * self._move_speed * frame_delay + self._pos
        rect = pygame.Rect(0, 0, 20, 5)
        rect.center = new_pos
        if tile_map.is_walkable(rect):
            self._pos = new_pos
            self._container.broadcast(self, ComponentMessageEnum.SET_LOCATION, self._pos)
            material = tile_map.get_material(rect)
            if material is not None and material != self._material:
                self._material = material
                print(f"I'm walking on {self._material}")

    def set_container(self, sprite: INotifierGameSprite):
        sprite.subscribe(ComponentMessageEnum.SET_VELOCITY, self)
        self._container = sprite


class TestGraphicsComponent(IGameSpriteGraphicsComponent, INotifiableComponent):

    _rect: pygame.Rect = pygame.Rect(90, 90, 20, 20)
    _foot: pygame.Rect = pygame.Rect(90, 105, 20, 5)

    def render(self, gfx: pygame.Surface):
        pygame.draw.circle(gfx, (0, 0, 255), self._rect.midtop, radius=10)
        pygame.draw.circle(gfx, (0, 0, 255), self._rect.center, radius=10)
        pygame.draw.rect(gfx, (255, 0, 255), self._foot, width=1)

    def set_container(self, sprite: INotifierGameSprite):
        sprite.subscribe(ComponentMessageEnum.SET_LOCATION, self)

    def notify(self, sender: object, msg_type: ComponentMessageEnum, value: any):
        self._foot.center = value
        self._rect.midbottom = self._foot.midbottom
