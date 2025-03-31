from importlib import resources
import pygame
from states.state import State
from config import cfg_item

class Intro(State):
    """
    Manages the introductory state, including menu options and user input handling.

    Attributes
    ----------
    font : pygame.font.Font
        Font used for rendering text.
    options : list of str
        List of menu options.
    selected_option : int
        Index of the currently selected menu option.
    next_state : str
        The next state to transition to.

    Methods
    -------
    enter():
        Initializes the state when entered.
    exit():
        Cleans up the state when exited.
    handle_input(event):
        Handles user input events for menu navigation.
    process_events(event):
        Processes various game events.
    update(delta_time):
        Updates the state with the given delta time.
    render(surface_dst):
        Renders the state on the given surface.
    release():
        Releases resources for the state.
    """

    def __init__(self):
        """
        Initializes the Intro state.
        """
        super().__init__()

        file_path = resources.files("assets.fonts").joinpath('Sansation.ttf')
        with resources.as_file(file_path) as font_image_path:
            self.font = pygame.font.Font(font_image_path, 32)

        self.options = ["Start Game"]
        self.selected_option = 0
        self.next_state = None

    def enter(self):
        """
        Initializes the state when entered.
        """
        self.done = False

    def exit(self):
        """
        Cleans up the state when exited.
        """
        pass

    def handle_input(self, event):
        """
        Handles user input events for menu navigation.

        Args:
            event (pygame.event.Event): The input event to handle.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                self.done = True
                if self.selected_option == 0:
                    self.next_state = "GamePlay"
                elif self.selected_option == 1:
                    self.next_state = "Options"
                elif self.selected_option == 2:
                    self.next_state = "Exit"

    def process_events(self, event):
        """
        Processes various game events.

        Args:
            event (pygame.event.Event): The game event to process.
        """
        pass

    def update(self, delta_time):
        """
        Updates the state with the given delta time.

        Args:
            delta_time (float): The time elapsed since the last update.
        """
        pass

    def render(self, surface_dst):
        """
        Renders the state on the given surface.

        Args:
            surface_dst (pygame.Surface): The surface to render on.
        """
        surface_dst.fill((0, 0, 0))  # Clear screen
        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i == self.selected_option else (100, 100, 100)
            text_surface = self.font.render(option, True, color)
            position = (cfg_item("game", "screen_size")[0] // 2 - text_surface.get_width() // 2,
                        cfg_item("game", "screen_size")[1] // 2 + i * 40)
            surface_dst.blit(text_surface, position)

    def release(self):
        """
        Releases resources for the state.
        """
        pass
