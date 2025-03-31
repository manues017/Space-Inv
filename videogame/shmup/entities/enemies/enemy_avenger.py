from importlib import resources
import random

import pygame

from shmup.entities.enemies.enemy import Enemy
from shmup.config import cfg_item


class EnemyAvenger(Enemy):
    """Class representing an Avenger enemy in the game.

    Attributes:
        __image : Static image used for all instances of EnemyAvenger.
        _fire_probability : Probability of the enemy firing a projectile.
    """

    __image = None

    def __init__(self, position_init, position_end):
        """Initializes an EnemyAvenger with initial and end positions.

        Args:
            position_init : Spawn position of the EnemyAvenger.
            position_end : End position where the EnemyAvenger will stop moving.
        """
        velocity_range = cfg_item("entities", "enemies", "avenger", "velocity_range")
        velocity = (random.uniform(velocity_range[0], velocity_range[1]), 0)

        self._fire_probability = cfg_item("entities", "enemies", "avenger", "fire_probability")

        if EnemyAvenger.__image is None:
            file_path = resources.files(cfg_item("entities", "enemies", "avenger", "image_file")[0]).joinpath(cfg_item("entities", "enemies", "avenger", "image_file")[1])
            with resources.as_file(file_path) as image_path:
                image = pygame.image.load(image_path).convert_alpha()
                EnemyAvenger.__image = pygame.transform.scale(image, (100, 60))

        super().__init__(position_init, position_end, velocity)

    @property
    def image(self):
        #The image used for the EnemyAvenger.
        return EnemyAvenger.__image