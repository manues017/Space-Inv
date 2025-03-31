import pygame
from importlib import resources

class BossShot(pygame.sprite.Sprite):
    """
    A class to represent the boss's shot in the game.

    Attributes
    ----------
    __image : pygame.Surface
        The image of the boss shot.

    Methods
    -------
    update(delta_time):
        Updates the position of the boss shot.
    get_image_height():
        Returns the height of the boss shot image.
    get_image_width():
        Returns the width of the boss shot image.
    __load_image():
        Loads and scales the image of the boss shot.
    """

    __image = None

    def __init__(self, position):
        """
        Constructs all the necessary attributes for the boss shot object.

        Parameters
        ----------
        position : tuple
            The initial position of the boss shot.
        """
        super().__init__()
        if BossShot.__image is None:
            self.__load_image()  # Ensure the image is loaded if it hasn't been already
        self.image = BossShot.__image  # Use the loaded and resized image
        self.rect = self.image.get_rect(topleft=position)
        self.__velocity = pygame.math.Vector2(0, 0.2)  # Adjust velocity as necessary

    def update(self, delta_time):
        """
        Updates the position of the boss shot.

        Parameters
        ----------
        delta_time : float
            The time elapsed since the last update.
        """
        self.rect.y += self.__velocity.y * delta_time  # Move the shot downwards
        if self.rect.y > pygame.display.get_surface().get_height():
            self.kill()  # Remove the shot if it goes off the screen

    @staticmethod
    def get_image_height():
        """
        Returns the height of the boss shot image.

        Returns
        -------
        int
            The height of the boss shot image.
        """
        if BossShot.__image is None:
            BossShot.__load_image()
        return BossShot.__image.get_height()

    @staticmethod
    def get_image_width():
        """
        Returns the width of the boss shot image.

        Returns
        -------
        int
            The width of the boss shot image.
        """
        if BossShot.__image is None:
            BossShot.__load_image()
        return BossShot.__image.get_width()

    @staticmethod
    def __load_image():
        """
        Loads and scales the image of the boss shot.
        """
        file_path = resources.files("shmup.assets.images").joinpath('boss-shot.png')
        with resources.as_file(file_path) as image_path:
            image = pygame.image.load(image_path).convert_alpha()
            BossShot.__image = pygame.transform.scale(image, (10, 40))  # Adjust size as necessary
