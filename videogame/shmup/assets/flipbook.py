import pygame

class FlipBook:

    def __init__(self, image_file, rows, cols):
        self.__image = pygame.image.load(image_file).convert_alpha()
        self.__sequence = []

        rect_width = self.__image.get_width() / cols
        rect_height = self.__image.get_height() / rows

        for row in range(rows):
            y = row * rect_height
            for col in range(cols):
                x = col * rect_width
                self.__sequence.append(pygame.Rect(x, y, rect_width, rect_height))

    def render(self, surface_dst, pos, sequence = 0):
        if sequence <= len(self.__sequence):
            surface_dst.blit(self.__image, pos, self.__sequence[sequence])