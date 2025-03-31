import random

import pygame

from falling_letters.config import cfg_item

class Letter:

    def __init__(self, text, font):
        color = (random.randint(cfg_item("letter", "color")[0], cfg_item("letter", "color")[1]), random.randint(cfg_item("letter", "color")[0], cfg_item("letter", "color")[1]), random.randint(cfg_item("letter", "color")[0], cfg_item("letter", "color")[1]))
        self.__image = font.render(f"{text}", True, color, None)
        scale_by = random.uniform(cfg_item("letter", "scale")[0], cfg_item("letter", "scale")[1])
        self.__image = pygame.transform.scale_by(self.__image, scale_by)
        self.__position = pygame.math.Vector2(random.randint(0, cfg_item("app", "screen_size")[0]), -cfg_item("letter", "margin"))
        self.__end_position = pygame.math.Vector2(self.__position.x, cfg_item("app", "screen_size")[1] + cfg_item("letter", "margin"))
        self.__speed = random.uniform(cfg_item("letter", "speed")[0], cfg_item("letter", "speed")[1])
        self.__is_alive = True

    def update(self, delta_time):
        self.__position.y += self.__speed * delta_time

        if self.__position.y >= self.__end_position.y:
            self.__is_alive = False

    def render(self, surface_dst):
        surface_dst.blit(self.__image, self.__position.xy)

    @property
    def is_alive(self):
        return self.__is_alive

    @is_alive.setter
    def is_alive(self, value):
        self.__is_alive = value