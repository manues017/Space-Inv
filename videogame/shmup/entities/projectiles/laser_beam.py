import pygame
import math
from importlib import resources
from shmup.entities.gameobject import GameObject
from shmup.config import cfg_item

class LaserBeam(pygame.sprite.Sprite):
    """Class representing a laser beam sprite.

    Attributes:
        __image (pygame.Surface): Class attribute holding the image for all instances.
        image (pygame.Surface): The image of the laser beam.
        rect (pygame.Rect): The rectangle representing the laser beam's position and size.
        movement_direction (int): The direction of the laser beam's movement.
        movement_timer (float): Timer to control the movement direction change.
    """
    
    __image = None

    def __init__(self, position):
        """Initializes a laser beam with the given position.

        Args:
            position (tuple): The initial position of the laser beam.
        """
    def __init__(self, position):
        super().__init__()
        if LaserBeam.__image is None:
            file_path = resources.files("shmup.assets.images").joinpath('laser-beam.png')
            with resources.as_file(file_path) as image_path:
                image = pygame.image.load(image_path).convert_alpha()
                image = pygame.transform.scale(image, (720, 100))  # Ajusta el tamaño según sea necesario
                LaserBeam.__image = pygame.transform.rotate(image, 90)
        self.image = LaserBeam.__image
        self.rect = self.image.get_rect(topleft=position)
        self._initial_x = self.rect.x
        self._movement_amplitude = 1  # Amplitud del movimiento
        self._movement_speed = 0.1  # Velocidad del movimiento
        self._movement_timer = 0   # Temporizador para el movimiento oscilatorio

    def update(self, delta_time):
        """Updates the laser beam's position.

        Args:
            delta_time (float): The time elapsed since the last update.
        """
        self._movement_timer += delta_time
        self.rect.x = self._initial_x + self._movement_amplitude * math.sin(self._movement_speed * self._movement_timer)
  

    def render(self, surface):
        """Renders the laser beam on the given surface.

        Args:
            surface (pygame.Surface): The surface on which to render the laser beam.
        """
        surface.blit(self.image, self.rect.topleft)

    @staticmethod
    def get_image_width():
        """Gets the width of the laser beam image.

        Returns:
            int: The width of the laser beam image.
        """
        return LaserBeam.__image.get_width()
