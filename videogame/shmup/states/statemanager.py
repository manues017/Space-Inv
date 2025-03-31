import pygame

from states.intro import Intro
from states.gameplay import GamePlay

class StateManager:

    def __init__(self):
        """
        Initializes the StateManager with the available states and sets the initial state.
        """
        self.__states = {
            "Intro": Intro(),
            "GamePlay": GamePlay()
        }

        self.__current_state_name = "Intro"
        self.__current_state = self.__states[self.__current_state_name]
        self.__current_state.enter()

    def process_events(self, event):
        """
        Processes events for the current state.

        Args:
            event (pygame.event.Event): The event to process.
        """
        if event.type == pygame.USEREVENT:
            self.__current_state.process_events(event)
        else:
            self.__current_state.handle_input(event)

    def update(self, delta_time):
        """
        Updates the current state and checks for state transitions.

        Args:
            delta_time (float): The time elapsed since the last update.
        """
        if self.__current_state.done:
            self.__change_state()

        self.__current_state.update(delta_time)

    def render(self, surface_dst):
        """
        Renders the current state on the given surface.

        Args:
            surface_dst (pygame.Surface): The surface to render on.
        """
        self.__current_state.render(surface_dst)

    def release(self):
        """
        Releases resources for the current state.
        """
        self.__current_state.release()
        self.__current_state.exit()

    def __change_state(self):
        """
        Changes the current state to the next state.
        """
        self.__current_state.exit()

        previous_state = self.__current_state_name
        self.__current_state_name = self.__current_state.next_state
        self.__current_state = self.__states[self.__current_state_name]
        self.__current_state.previous_state = previous_state

        self.__current_state.enter()
        
    def get_state(self):
        """
        Returns the current state instance.

        Returns:
            State: The current state instance.
        """
        return self.__current_state