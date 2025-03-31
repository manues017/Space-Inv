from importlib import resources

import pygame

from shmup.entities.projectiles.projectile import Projectile
from shmup.entities.projectiles.projectile_type import ProjectileType
from shmup.config import cfg_item

class ProjectileAllied(Projectile):
    """Class representing an allied projectile.

    Attributes:
        __image (pygame.Surface): Class attribute holding the image for all instances.
        image (pygame.Surface): The image of the allied projectile.
    """
    
    __image = None

    def __init__(self, position):
        """Initializes an allied projectile with the given position.

        Args:
            position (tuple): The initial position of the allied projectile.
        """
        velocity = cfg_item("entities", "projectiles", "allied", "velocity")

        if ProjectileAllied.__image is None:
            file_path = resources.files(cfg_item("entities", "projectiles", "allied", "image_file")[0]).joinpath(cfg_item("entities", "projectiles", "allied", "image_file")[1])
            with resources.as_file(file_path) as image_path:
                ProjectileAllied.__image = pygame.image.load(image_path).convert_alpha()

        super().__init__(position, velocity)

    @property
    def image(self):
        """Gets the image of the allied projectile.

        Returns:
            pygame.Surface: The image of the allied projectile.
        """
        return ProjectileAllied.__image

    @property
    def proj_type(self):
        """Gets the type of the projectile.

        Returns:
            ProjectileType: The type of the projectile, which is Allied.
        """
        return ProjectileType.Allied