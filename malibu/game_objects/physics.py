import pygame

from ..services import ServiceLocator
from ..typing import IBehaviorComponent, IWorldMap, IGameObject
from ..enum import StateEnum


class BasicPhysicsComponent(IBehaviorComponent):

    parent: IGameObject = None
    move_speed = 150.0
    velocity: pygame.Vector2 = pygame.Vector2(0)
    material: str = None

    def update(self, frame_delta: float, world: IWorldMap):

        vector: pygame.Vector2 = self.parent.get_state(StateEnum.TARGET_VECTOR)
        if vector == (0, 0):
            return

        new_fp: pygame.Rect = self.parent.get_state(StateEnum.FOOTPRINT).copy()
        new_fp.center = vector * self.move_speed * frame_delta + pygame.Vector2(new_fp.center)
        new_location = pygame.Vector2(new_fp.center)
        if world.is_walkable(new_fp):
            self.parent.set_state(StateEnum.WORLD_LOCATION, new_location)

        material = world.get_material(new_fp)
        if material != self.material:
            self.material = material
            self.parent.set_state(StateEnum.UPON_MATERIAL, material)

        # TODO: Material?
        ServiceLocator.get_audio().enqueue("grass-footsteps", new_location)

    def set_parent(self, game_object: IGameObject):
        self.parent = game_object

    def _set_location(self, location: pygame.Vector2):
        self.parent.set_state(StateEnum.WORLD_LOCATION, location)
