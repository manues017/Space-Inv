from importlib import resources

import pygame

from assets.flipbook import FlipBook
from entities.gameobject import GameObject
from config import cfg_item
from events import Events

class Explosion(GameObject):
    """Represents an explosion animation in the game.

    Attributes:
        __time_per_sequence (int): The time per sequence frame in the explosion animation.
        __flipbook (FlipBook): The flipbook object that handles the explosion animation frames.
        __total_sequences (int): The total number of sequences in the explosion animation.
        __current_sequence (int): The current sequence frame being displayed.
        __current_time (int): The current time elapsed since the last sequence frame change.
        _position (tuple): The position of the explosion.
    """

    def __init__(self, position):
        """Initializes a new Explosion instance.

        Args:
            position (tuple): The initial position of the explosion.
        """
        super().__init__()
        self.__time_per_sequence = cfg_item("entities", "explosion", "time_per_sequence")
        size = cfg_item("entities", "explosion", "size")

        file_path = resources.files(cfg_item("entities", "explosion", "image_file")[0]).joinpath(cfg_item("entities", "explosion", "image_file")[1])
        with resources.as_file(file_path) as image_path:
            self.__flipbook = FlipBook(image_path, size[0], size[1])

        self.__total_sequences = size[0] * size[1]
        self.__current_sequence = 0
        self.__current_time = 0
        self._position = position

    def handle_input(self, key, is_pressed):
        """Handles input events. Not used for explosions.

        Args:
            key (int): The key code of the pressed/released key.
            is_pressed (bool): Whether the key is pressed or released.
        """
        pass

    def process_events(self, event):
        """Processes other game events. Not used for explosions.

        Args:
            event (pygame.event.Event): The event to process.
        """
        pass

    def update(self, delta_time):
        """Updates the explosion animation based on the elapsed time.

        Args:
            delta_time (float): The time elapsed since the last update.
        """
        self.__current_time += delta_time
        if self.__current_time >= self.__time_per_sequence:
            self.__current_time -= self.__time_per_sequence
            self.__current_sequence += 1
            if self.__current_sequence >= self.__total_sequences - 1:
                end_event = pygame.event.Event(pygame.USEREVENT, event=Events.EXPLOSION_FINISHED, explosion=self)
                pygame.event.post(end_event)

    def render(self, surface_dst):
        """Renders the explosion animation on the given surface.

        Args:
            surface_dst (pygame.Surface): The surface to render the explosion on.
        """
        self.__flipbook.render(surface_dst, self._position, self.__current_sequence)

    def release(self):
        """Releases any resources held by the explosion. Not used."""
        pass
