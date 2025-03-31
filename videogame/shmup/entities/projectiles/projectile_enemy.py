from importlib import resources

import pygame

from shmup.entities.projectiles.projectile import Projectile
from shmup.entities.projectiles.projectile_type import ProjectileType
from shmup.config import cfg_item

class ProjectileEnemy(Projectile):
    """Class representing an enemy projectile.

    Attributes:
        __image (pygame.Surface): Class attribute holding the image for all instances.
        image (pygame.Surface): The image of the enemy projectile.
    """
    
    __image = None

    def __init__(self, position):
        """Initializes an enemy projectile with the given position.

        Args:
            position (tuple): The initial position of the enemy projectile.
        """
        velocity = cfg_item("entities", "projectiles", "enemy", "velocity")

        if ProjectileEnemy.__image is None:
            file_path = resources.files(cfg_item("entities", "projectiles", "enemy", "image_file")[0]).joinpath(cfg_item("entities", "projectiles", "enemy", "image_file")[1])
            with resources.as_file(file_path) as image_path:
                image = pygame.image.load(image_path).convert_alpha()
                ProjectileEnemy.__image = pygame.transform.scale(image, (40, 40))

        super().__init__(position, velocity)

    @property
    def image(self):
        """Gets the image of the enemy projectile.

        Returns:
            pygame.Surface: The image of the enemy projectile.
        """
        return ProjectileEnemy.__image

    @property
    def proj_type(self):
        """Gets the type of the projectile.

        Returns:
            ProjectileType: The type of the projectile, which is Enemy.
        """
        return ProjectileType.Enemy
