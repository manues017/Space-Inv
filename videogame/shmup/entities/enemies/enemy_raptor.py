from importlib import resources
import random
import pygame
from entities.enemies.enemy import Enemy
from config import cfg_item


class EnemyRaptor(Enemy):
    """Class representing a Raptor enemy in the game.

    Attributes:
        __image : Static image used for all instances of EnemyRaptor.
        _fire_probability : Probability of the enemy firing a projectile.
        _image : Image used for the instance of EnemyRaptor.
    """

    __image = None

    def __init__(self, position_init, position_end):
        """Initializes an EnemyRaptor with initial and end positions.

        Args:
            position_init : Spawn position of the EnemyRaptor.
            position_end : End position where the EnemyRaptor will stop moving.
        """
        velocity_range = cfg_item("entities", "enemies", "raptor", "velocity_range")
        velocity = (0, random.uniform(velocity_range[0], velocity_range[1]))

        self._fire_probability = cfg_item("entities", "enemies", "raptor", "fire_probability")

        if EnemyRaptor.__image is None:
            file_path = resources.files(cfg_item("entities", "enemies", "raptor", "image_file")[0]).joinpath(cfg_item("entities", "enemies", "raptor", "image_file")[1])
            with resources.as_file(file_path) as image_path:
                image = pygame.image.load(image_path).convert_alpha()
                image = pygame.transform.flip(image, False, True)
                EnemyRaptor.__image = pygame.transform.scale(image, (50, 50))  

        # Use the resized image in the instance
        self._image = EnemyRaptor.__image  
        
        super().__init__(position_init, position_end, velocity)
        self.rect_sync()  

    @property
    def image(self):
        """pygame.Surface: The image used for the instance of EnemyRaptor."""
        return self._image
