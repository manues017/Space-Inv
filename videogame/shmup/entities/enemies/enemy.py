import random

import pygame

from shmup.entities.gameobject import GameObject
from shmup.events import Events
from shmup.config import cfg_item


class Enemy(GameObject):
    """Base class for enemy entities in the game.

    Attributes:
        _position (pygame.math.Vector2): The current position of the enemy.
        __position_end (pygame.math.Vector2): The end position where the enemy stops moving.
        __velocity (pygame.math.Vector2): The velocity of the enemy.
        _fire_probability (float): The probability of the enemy firing a projectile.
     """

    def __init__(self, position_init, position_end, velocity):
        """Initializes an enemy with positions and velocity.

        Args:
            position_init (tuple): The initial position of the enemy.
            position_end (tuple): The end position where the enemy will stop moving.
            velocity (tuple): The velocity of the enemy.
        """
        super().__init__()
        self._position = pygame.math.Vector2(position_init)
        self.__position_end = pygame.math.Vector2(position_end)
        self.__velocity = pygame.math.Vector2(velocity)
        self.rect_sync()

    def handle_input(self, key, is_pressed):
        """Handles input events.

        Args:
            key (int): The key that was pressed or released.
            is_pressed (bool): Whether the key is pressed or released.
        """
        pass

    def process_events(self, event):
        """Processes game events.

        Args:
            event (pygame.event.Event): The event to process.
        """
        pass

    def update(self, delta_time):
        """Updates the enemy's position and state.

        Args:
            delta_time (float): The time elapsed since the last update.
        """
        distance = self.__velocity * delta_time
        self._position += distance
        screen_width = cfg_item('game', 'screen_size')[0]
        
        if self._position.x <= 0 or self._position.x >= screen_width - self.image.get_width():
            self.__velocity.x = -self.__velocity.x

        self.__check_end_point()
        self.__fire()
        self.rect_sync()

    def render(self, surface_dst):
        """Renders the enemy on the given surface.

        Args:
            surface_dst (pygame.Surface): The surface on which to render the enemy.
        """
        surface_dst.blit(self.image, self._position)

    def release(self):
        """Releases resources held by the enemy."""
        pass

    def __check_end_point(self):
        """Checks if the enemy has reached its end point and posts an event if true."""
        if abs(self.__position_end.y - self._position.y) <= cfg_item("entities", "enemies", "delta_oos"):
            kill_event = pygame.event.Event(pygame.USEREVENT, event=Events.ENEMY_END_POINT, enemy=self)
            pygame.event.post(kill_event)

    def __fire(self):
        """Fires a projectile with a certain probability and posts an event."""
        if random.random() <= self._fire_probability:
            x = self._position.x + (self.image.get_width() // 2)
            y = self._position.y + self.image.get_height()
            fire_event = pygame.event.Event(pygame.USEREVENT, event=Events.ENEMY_FIRES, pos=(x, y))
            pygame.event.post(fire_event)