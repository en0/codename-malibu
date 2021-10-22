import pygame

from .base import GameComponentBase, SubMap_T
from ..enum import ComponentMessageEnum
from ..typing import IPhysicsComponent, IWorldMap


class BasicPhysicsComponent(GameComponentBase, IPhysicsComponent):

    move_speed = 150.0
    velocity: pygame.Vector2 = pygame.Vector2(0)
    location: pygame.Vector2 = pygame.Vector2(100.0, 100.0)
    material: str = None

    subscriptions = [
        ComponentMessageEnum.SET_VELOCITY,
    ]

    def set_velocity(self, sender: object, value: pygame.Vector2):
        self.velocity = value

    def update(self, frame_delta: float, world: IWorldMap):
        rect = pygame.Rect(0.0, 0.0, 20, 20)
        new_location = self.velocity * self.move_speed * frame_delta + self.location
        rect.center = new_location
        if world.is_walkable(rect):
            self.location = new_location
            self.parent.receive_message(self, ComponentMessageEnum.SET_LOCATION, self.location)
            material = world.get_material(rect)
            if material != self.material:
                self.material = material
                print(f"I'm walking on {material}")

