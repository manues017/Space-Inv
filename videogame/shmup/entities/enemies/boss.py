import pygame
from shmup.entities.gameobject import GameObject
from shmup.config import cfg_item
from importlib import resources
from shmup.events import Events
from shmup.entities.projectiles.laser_beam import LaserBeam
from shmup.entities.projectiles.boss_shot import BossShot
import random

class Boss(GameObject):
    """
    A class to represent the boss enemy in the game.

    Attributes
    ----------
    __image : pygame.Surface
        The image of the boss.
    _position : pygame.math.Vector2
        The position of the boss on the screen.
    __position_end : pygame.math.Vector2
        The target position for the boss to move to.
    __velocity : pygame.math.Vector2
        The velocity of the boss.
    __health : int
        The health of the boss.
    __attack_patterns : list
        List of attack pattern methods.
    __current_attack_pattern : method
        The current attack pattern being used.
    __attack_timer : float
        Timer for attack pattern switching.
    laser_beams : pygame.sprite.Group
        Group to manage laser beams and shots fired by the boss.
    __is_oscillating : bool
        Flag to determine if the boss is oscillating due to damage.
    __oscillation_timer : float
        Timer for oscillation effect.
    __oscillation_duration : float
        Duration of the oscillation effect.
    __oscillation_magnitude : int
        Magnitude of the oscillation effect.
    __oscillation_direction : int
        Direction of the oscillation effect.

    Methods
    -------
    update(delta_time):
        Updates the position and state of the boss.
    render(surface_dst):
        Renders the boss and its shots on the given surface.
    release():
        Releases resources held by the boss.
    handle_input(key, is_pressed):
        Handles player input (not used for boss).
    process_events(event):
        Processes events (not used for boss).
    take_damage(damage):
        Reduces the boss's health and triggers oscillation on damage.
    kill():
        Kills the boss and triggers the BOSS_KILLED event.
    __start_oscillation():
        Starts the oscillation effect for the boss.
    __attack_pattern_1():
        Executes the first attack pattern (fires a random shot).
    __attack_pattern_2():
        Executes the second attack pattern (fires a random shot).
    __attack_pattern_3():
        Executes the third attack pattern (fires laser beams).
    __fire_boss_shot():
        Fires a shot from a random position on the boss.
    __fire_laser_beam():
        Fires laser beams from the sides of the screen.
    """

    __image = None

    def __init__(self, position_init, position_end):
        """
        Initializes the boss with the given initial and target positions.

        Parameters
        ----------
        position_init : tuple
            The initial position of the boss.
        position_end : tuple
            The target position of the boss.
        """
        super().__init__()
        self._position = pygame.math.Vector2(position_init)
        self.__position_end = pygame.math.Vector2(position_end)
        self.__velocity = pygame.math.Vector2(0, 0.05)
        
        self.__health = cfg_item('entities','boss', 'health')
        self.__attack_patterns = [self.__attack_pattern_1, self.__attack_pattern_2, self.__attack_pattern_3]
        self.__current_attack_pattern = random.choice(self.__attack_patterns)
        self.__attack_timer = 0
        
        self.laser_beams = pygame.sprite.Group()

        # Oscillation properties
        self.__is_oscillating = False
        self.__oscillation_timer = 0
        self.__oscillation_duration = 0.5  # Duration of the oscillation in seconds
        self.__oscillation_magnitude = 5  # Magnitude of the oscillation
        self.__oscillation_direction = 1  # Direction of the oscillation

        if Boss.__image is None:
            file_path = resources.files(cfg_item("entities", "boss", "image_file")[0]).joinpath(cfg_item("entities", "boss", "image_file")[1])
            with resources.as_file(file_path) as image_path:
                image = pygame.image.load(image_path).convert_alpha()
                Boss.__image = pygame.transform.scale(image, (400, 300))
                print("Boss image loaded")

        self.rect_sync()

    def update(self, delta_time):
        """
        Updates the position and state of the boss.

        Parameters
        ----------
        delta_time : float
            The time elapsed since the last update.
        """
        if self._position.y < self.__position_end.y:
            distance = self.__velocity * delta_time
            self._position += distance
            if self._position.y >= self.__position_end.y:
                self._position.y = self.__position_end.y
        else:
            self.__attack_timer += delta_time
            if self.__attack_timer >= cfg_item('entities', 'boss', 'attack_interval'):
                self.__current_attack_pattern()
                self.__current_attack_pattern = random.choice(self.__attack_patterns)
                self.__attack_timer = 0

        self.laser_beams.update(delta_time)
        self.rect_sync()

        # Handle oscillation
        if self.__is_oscillating:
            self.__oscillation_timer += delta_time
            oscillation_offset = self.__oscillation_magnitude * self.__oscillation_direction
            self._position.x += oscillation_offset

            if self.__oscillation_timer >= self.__oscillation_duration:
                self.__is_oscillating = False
                self.__oscillation_timer = 0
                self._position.x = self.__original_position.x
            else:
                self.__oscillation_direction *= -1

    def render(self, surface_dst):
        """
        Renders the boss and its shots on the given surface.

        Parameters
        ----------
        surface_dst : pygame.Surface
            The surface to render the boss and its shots on.
        """
        surface_dst.blit(Boss.__image, self._position)
        self.laser_beams.draw(surface_dst)

    def release(self):
        """
        Releases resources held by the boss.
        """
        pass

    def handle_input(self, key, is_pressed):
        """
        Handles player input (not used for boss).

        Parameters
        ----------
        key : int
            The key that was pressed or released.
        is_pressed : bool
            Whether the key was pressed or released.
        """
        pass

    def process_events(self, event):
        """
        Processes events (not used for boss).

        Parameters
        ----------
        event : pygame.event.Event
            The event to process.
        """
        pass

    @property
    def image(self):
        """
        Returns the image of the boss.

        Returns
        -------
        pygame.Surface
            The image of the boss.
        """
        return Boss.__image

    def take_damage(self, damage):
        """
        Reduces the boss's health and triggers oscillation on damage.

        Parameters
        ----------
        damage : int
            The amount of damage to inflict on the boss.
        """
        self.__health -= damage
        print(f"Boss Health: {self.__health}")
        if self.__health <= 0:
            self.__health = 0
            self.kill()
        else:
            self.__start_oscillation()

    def kill(self):
        """
        Kills the boss and triggers the BOSS_KILLED event.
        """
        kill_event = pygame.event.Event(pygame.USEREVENT, event=Events.BOSS_KILLED, boss=self)
        pygame.event.post(kill_event)
        super().kill()

    def __start_oscillation(self):
        """
        Starts the oscillation effect for the boss.
        """
        self.__is_oscillating = True
        self.__oscillation_timer = 0
        self.__original_position = self._position.copy()

    def __attack_pattern_1(self):
        """
        Executes the first attack pattern (fires a random shot).
        """
        self.__fire_boss_shot()
        print("Boss performs attack pattern 1")

    def __attack_pattern_2(self):
        """
        Executes the second attack pattern (fires a random shot).
        """
        self.__fire_boss_shot()
        print("Boss performs attack pattern 2")

    def __attack_pattern_3(self):
        """
        Executes the third attack pattern (fires laser beams).
        """
        self.__fire_laser_beam()
        print("Boss performs attack pattern 3")

    def __fire_boss_shot(self):
        """
        Fires a shot from a random position on the boss.
        """
        boss_width = Boss.__image.get_width()
        boss_height = Boss.__image.get_height()
        shot_x = random.randint(0, boss_width)
        shot_position = (self._position.x + shot_x, self._position.y + boss_height)
        boss_shot = BossShot(shot_position)
        self.laser_beams.add(boss_shot)
        print("Firing boss shot")

    def __fire_laser_beam(self):
        """
        Fires laser beams from the sides of the screen.
        """
        screen_height = cfg_item("game", "screen_size")[1]
        left_beam = LaserBeam((0, self._position.y))
        right_beam = LaserBeam((cfg_item("game", "screen_size")[0] - LaserBeam.get_image_width(), self._position.y))
        self.laser_beams.add(left_beam)
        self.laser_beams.add(right_beam)
        print("Firing laser beams")