from importlib import resources

import pygame

from shmup.config import cfg_item
from shmup.entities.gameobject import GameObject
from shmup.events import Events
from .movement_type import MovementType

class Hero(GameObject):
    """
    Represents the hero character in the game.

    Attributes:
        __hero_image_height (int): The height of the hero's image.
        __hero_spawn (int): The initial spawn position of the hero.
        __hero_is_moving_up (bool): Whether the hero is moving up.
        __hero_is_moving_down (bool): Whether the hero is moving down.
        __hero_is_moving_left (bool): Whether the hero is moving left.
        __hero_is_moving_right (bool): Whether the hero is moving right.
        __movement_type (MovementType): The type of movement allowed for the hero.
        __speed (float): The speed of the hero.
        __cool_down (float): The cooldown time for shooting.
        __shoot_sound (pygame.mixer.Sound): The sound played when the hero shoots.
    """

    def __init__(self, movement_type):
        """
        Initializes the hero character.

        Args:
            movement_type (MovementType): The type of movement allowed for the hero.
        """
        super().__init__()
        
        # Load the hero image
        file_path = resources.files("shmup.assets.images").joinpath('hero.png')
        with resources.as_file(file_path) as hero_image_path:
            self._image = pygame.image.load(hero_image_path).convert_alpha()
        
        # Use the image height to calculate the initial position
        self.__hero_image_height = self._image.get_height()
        self.__hero_spawn = cfg_item("game", "screen_size")[1] - self.__hero_image_height  # Adjust initial position
        
        # Set the initial position of the hero
        self._position = pygame.math.Vector2(cfg_item("game", "screen_size")[0]/2, self.__hero_spawn)

        self.__hero_is_moving_up = False
        self.__hero_is_moving_down = False
        self.__hero_is_moving_left = False
        self.__hero_is_moving_right = False

        self.__movement_type = movement_type

        self.__speed = 0.3
        self.__cool_down = 0
        
        sound_path = resources.files("shmup.assets.sounds").joinpath('shot.mp3')
        with resources.as_file(sound_path) as shoot_sound_path:
            self.__shoot_sound = pygame.mixer.Sound(shoot_sound_path)

        self.rect_sync()

    def handle_input(self, key, is_pressed):
        """
        Handles player input.

        Args:
            key (int): The key pressed by the player.
            is_pressed (bool): Whether the key is pressed or released.
        """
        # Handle input for the object's movement according to its restrictions
        
        # Vertical movement logic
        if self.__movement_type in (MovementType.BOTH, MovementType.VERTICAL):
            if key == pygame.K_UP:
                self.__hero_is_moving_up = is_pressed
            if key == pygame.K_DOWN:
                self.__hero_is_moving_down = is_pressed
        
        # Horizontal movement logic        
        if self.__movement_type in (MovementType.BOTH, MovementType.HORIZONTAL):
            if key == pygame.K_LEFT:
                self.__hero_is_moving_left = is_pressed
            if key == pygame.K_RIGHT:
                self.__hero_is_moving_right = is_pressed
        
        if key == pygame.K_SPACE:
            if self.__cool_down <= 0.0:
                self.__fire()

    def process_events(self, event):
        """
        Processes events.

        Args:
            event (pygame.event.Event): The event to process.
        """
        pass

    def update(self, delta_time):
        """
        Updates the hero's state.

        Args:
            delta_time (float): The time elapsed since the last update.
        """
        velocity = pygame.math.Vector2(0, 0)

        if self.__hero_is_moving_up:
            velocity.y -= self.__speed
        if self.__hero_is_moving_down:
            velocity.y += self.__speed
        if self.__hero_is_moving_left:
            velocity.x -= self.__speed
        if self.__hero_is_moving_right:
            velocity.x += self.__speed
        self._position += velocity * delta_time
        
        if self._position.x >= cfg_item('game','screen_size')[0] - cfg_item('entities', 'hero', 'width'):
            self._position.x = cfg_item('game','screen_size')[0] - cfg_item('entities', 'hero', 'width')
            
        if self._position.x <= cfg_item('game','screen_size_min'):
            self._position.x = cfg_item('game','screen_size_min')

        if self.__cool_down >= 0.0:
            self.__cool_down -= delta_time

        self.rect_sync()

    def render(self, surface_dst):
        """
        Renders the hero on the given surface.

        Args:
            surface_dst (pygame.Surface): The surface to render the hero on.
        """
        surface_dst.blit(self._image, self._position.xy)

    def release(self):
        """
        Releases any resources held by the hero.
        """
        pass

    def __fire(self):
        """
        Fires a projectile from the hero's current position.
        """
        self.__cool_down = cfg_item("entities", "hero", "cool_down_time")
        x = self._position.x + (self._image.get_width() // 2)

        fire_event = pygame.event.Event(pygame.USEREVENT, event = Events.HERO_FIRES, pos = (x, self._position.y))
        pygame.event.post(fire_event)
        
        self.__shoot_sound.play()
        
    @property
    def image(self):
        """
        Returns the hero's image.

        Returns:
            pygame.Surface: The image of the hero.
        """
        return self._image
