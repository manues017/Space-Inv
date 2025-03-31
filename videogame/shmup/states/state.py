from abc import ABC, abstractmethod

class State(ABC):
    """
    An abstract base class for defining game states.

    Attributes
    ----------
    done : bool
        Indicates whether the state has completed its tasks.
    next_state : str
        The identifier of the next state to transition to.
    previous_state : str
        The identifier of the previous state.

    Methods
    -------
    enter():
        Abstract method to initialize the state when entered.
    exit():
        Abstract method to clean up the state when exited.
    handle_input(key, is_pressed):
        Abstract method to handle user input.
    process_events(event):
        Abstract method to process various game events.
    update(delta_time):
        Abstract method to update the state with the given delta time.
    render(surface_dst):
        Abstract method to render the state on the given surface.
    release():
        Abstract method to release resources for the state.
    """


    def __init__(self):
        self.done = False
        self.next_state = ""
        self.previous_state = ""

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def exit(self):
        pass

    @abstractmethod
    def handle_input(self, key, is_pressed):
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