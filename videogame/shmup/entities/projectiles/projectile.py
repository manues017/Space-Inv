import pygame

from entities.gameobject import GameObject
from events import Events
from config import cfg_item

class Projectile(GameObject):
    """Represents a projectile in the game.

    Attributes:
        _position (pygame.math.Vector2): The current position of the projectile.
        __velocity (pygame.math.Vector2): The velocity of the projectile.
    """

    def __init__(self, position, velocity):
        """Initializes a new Projectile instance.

        Args:
            position (tuple): The initial position of the projectile.
            velocity (tuple): The velocity of the projectile.
        """
        super().__init__()
        self._position = pygame.math.Vector2(position)
        self.__velocity = pygame.math.Vector2(velocity)
        self.rect_sync()

    def handle_input(self, key, is_pressed):
        """Handles input events. Not used for projectiles.

        Args:
            key (int): The key code of the pressed/released key.
            is_pressed (bool): Whether the key is pressed or released.
        """
        pass

    def process_events(self, event):
        """Processes other game events. Not used for projectiles.

        Args:
            event (pygame.event.Event): The event to process.
        """
        pass

    def update(self, delta_time):
        """Updates the projectile's position based on its velocity.

        Args:
            delta_time (float): The time elapsed since the last update.
        """
        distance = self.__velocity * delta_time

        if self._in_bounds(distance):
            self._position += distance
        else:
            kill_event = pygame.event.Event(pygame.USEREVENT, event=Events.PROJECTILE_OUT_OF_SCREEN, proj=self)
            pygame.event.post(kill_event)

        self.rect_sync()

    def render(self, surface_dst):
        """Renders the projectile on the given surface.

        Args:
            surface_dst (pygame.Surface): The surface to render the projectile on.
        """
        surface_dst.blit(self.image, self._position)

    def release(self):
        """Releases any resources held by the projectile. Not used."""
        pass

    def _in_bounds(self, distance):
        """Checks if the projectile is within the screen bounds after moving.

        Args:
            distance (pygame.math.Vector2): The distance to move the projectile.

        Returns:
            bool: True if the projectile is within bounds, False otherwise.
        """
        new_position = self._position + distance
        screen_size = cfg_item("game", "screen_size")
        return 0 <= new_position.x <= screen_size[0] and 0 <= new_position.y <= screen_size[1]
