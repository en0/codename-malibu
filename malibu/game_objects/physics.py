import pygame

from ..services import ServiceLocator
from ..typing import IBehaviorComponent, IWorldMap, IGameObject


class BasicPhysicsComponent(IBehaviorComponent):

    parent: IGameObject = None
    move_speed = 150.0
    velocity: pygame.Vector2 = pygame.Vector2(0)
    material: str = None

    def update(self, frame_delta: float, world: IWorldMap):

        moving = False
        rect = self.parent.data.footprint.copy()
        new_location = self.parent.data.transform * self.move_speed * frame_delta + self.parent.data.location
        rect.center = new_location
        if world.is_walkable(rect):
            self._set_location(new_location)
            moving = self.parent.data.transform != (0, 0)

        material = world.get_material(rect)
        if material != self.material:
            self._set_material(material)

        if moving:
            # TODO: Material?
            ServiceLocator.get_audio().enqueue("grass-footsteps", self.parent.data.location)

    def set_parent(self, game_object: IGameObject):
        self.parent = game_object

    def _set_location(self, location: pygame.Vector2):
        self.parent.data.location = pygame.Vector2(location)

    def _set_material(self, material: str):
        self.material = material
        print(f"I'm walking on {material}")
