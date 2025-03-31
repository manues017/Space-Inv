import pygame

class RenderGroup(pygame.sprite.Group):
    """
    A group to manage multiple game objects, handling their input, events, rendering, and releasing resources.

    Methods
    -------
    handle_input(key, is_pressed):
        Handles player input for all sprites in the group.
    process_events(event):
        Processes events for all sprites in the group.
    render(surface_dst):
        Renders all sprites in the group on the given surface.
    release():
        Releases resources for all sprites in the group.
    """

    def __init__(self):
        """
        Initializes the RenderGroup.
        """
        super().__init__()

    def handle_input(self, key, is_pressed):
        """
        Handles player input for all sprites in the group.

        Args:
            key (int): The key pressed by the player.
            is_pressed (bool): Whether the key is pressed or released.
        """
        for sprite in self.sprites():
            sprite.handle_input(key, is_pressed)

    def process_events(self, event):
        """
        Processes events for all sprites in the group.

        Args:
            event (pygame.event.Event): The event to process.
        """
        for sprite in self.sprites():
            sprite.process_events(event)

    def render(self, surface_dst):
        """
        Renders all sprites in the group on the given surface.

        Args:
            surface_dst (pygame.Surface): The surface to render the sprites on.
        """
        for sprite in self.sprites():
            sprite.render(surface_dst)

    def release(self):
        """
        Releases resources for all sprites in the group.
        """
        for sprite in self.sprites():
            sprite.release()
