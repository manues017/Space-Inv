from importlib import resources

import pygame

from falling_letters.entities.letter import Letter
from falling_letters.config import cfg_item

class Manager:

    def __init__(self):
        file_path = resources.files(cfg_item("font", "filename")[0]).joinpath(cfg_item("font", "filename")[1])
        with resources.as_file(file_path) as font_image_path:
            self.__font = pygame.font.Font(font_image_path, cfg_item("font", "size"))

        self.__letters = []

    def handle_input(self, event):
        self.__spawn_letter(event.unicode)

    def update(self, delta_time):
        for letter in self.__letters.copy():
            letter.update(delta_time)
            if not letter.is_alive:
                self.__letters.remove(letter)

    def render(self, surface_dst):
        for letter in self.__letters:
            letter.render(surface_dst)

    def __spawn_letter(self, text):
        self.__letters.append(Letter(text, self.__font))
        print(f"{len(self.__letters)}")