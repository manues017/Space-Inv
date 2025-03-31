from abc import ABC, abstractmethod

import pygame

from config import cfg_item

class GameObject(pygame.sprite.Sprite, ABC):
    """
    An abstract class to represent a virtual game object.

    Attributes
    ----------
    _position : pygame.math.Vector2
        position of the game object in the screen
    _image : pygame.Surface
        loaded image of the game object

    Methods
    -------
    handle_input(key, is_pressed):
        Abstract, handles the input of the player
    process_events(event):
        Abstract, process events for other parts of the app
    update(delta_time):
        Abstract, updates the game object for a period of time
    release():
        Abstract, releases any resource from the game object
    _in_bounds(distance):
        Checks if game object is inside the screen
    """

    def __init__(self):
        """
        Abstract, Constructs the game object class
        """
        super().__init__()
        self._position = pygame.math.Vector2(0.0, 0.0)
        self.rect = pygame.Rect(0,0,0,0)

    @abstractmethod
    def handle_input(self, key, is_pressed):
        """
        Abstract, handles the input of the player

        Parameters
        ----------
        key : pygame.key
            key pressed by the player
        is_pressed : boolean
            if key is pressed or released
        """
        pass

    @abstractmethod
    def process_events(self, event):
        pass

    @abstractmethod
    def update(self, delta_time):
        pass

    @abstractmethod
    def render(self, surface_dst):
        pass

    @abstractmethod
    def release(self):
        pass

    def _in_bounds(self, distance):
        """
        Checks if the game object is within the screen bounds.

        Parameters:
            distance (pygame.math.Vector2): The distance to move the game object.

        Returns:
            bool: True if the game object is within bounds, False otherwise.
        """
        new_pos = self._position + distance
        screen_width, screen_height = cfg_item("game", "screen_size")
        return 0 <= new_pos.x <= screen_width and 0 <= new_pos.y <= screen_height

    @property
    def pos(self):
        """
        Returns the position of the game object.

        Returns:
            pygame.math.Vector2: The position of the game object.
        """
        return self._position

    def rect_sync(self):
        """
        Synchronizes the rectangle's position and dimensions with the game object's image.
        """
        self.rect.x = self._position.x
        self.rect.y = self._position.y
        self.rect.height = self.image.get_height()
        self.rect.width = self.image.get_width()