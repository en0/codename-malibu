import pygame

from .base import GameComponentBase, SubMap_T
from ..enum import GameObjectMessageEnum
from ..typing import IPhysicsComponent, IWorldMap


class BasicPhysicsComponent(GameComponentBase, IPhysicsComponent):

    move_speed = 150.0
    velocity: pygame.Vector2 = pygame.Vector2(0)
    location: pygame.Vector2 = pygame.Vector2(100.0, 100.0)
    material: str = None

    subscriptions = [
        GameObjectMessageEnum.SET_VELOCITY,
        GameObjectMessageEnum.SET_LOCATION,
    ]

    def on_set_velocity(self, sender: object, value: pygame.Vector2):
        self.velocity = value

    def on_set_location(self, sender: object, value: pygame.Vector2):
        self._set_location(value)

    def update(self, frame_delta: float, world: IWorldMap):

        rect = pygame.Rect(0.0, 0.0, 20, 20)
        new_location = self.velocity * self.move_speed * frame_delta + self.location
        rect.center = new_location
        if world.is_walkable(rect):
            self._set_location(new_location)

        material = world.get_material(rect)
        if material != self.material:
            self._set_material(material)

    def _set_location(self, location: pygame.Vector2):
        self.location = location
        self.parent.receive_message(self, GameObjectMessageEnum.SET_LOCATION, location)

    def _set_material(self, material: str):
        self.material = material
        self.parent.receive_message(self, GameObjectMessageEnum.SET_STANDING_ON_MATERIAL, material)
        print(f"I'm walking on {material}")

