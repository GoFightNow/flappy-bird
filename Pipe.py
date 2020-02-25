# Created by Go_Fight_Now on 2019/12/8 16:32. #
# -*- coding:utf-8 -*-
import pygame, random
from pygame.locals import *
from pygame import Surface


class Pipe:

    def __init__(self, temp_screen, pipe_type) -> None:
        self.screen: Surface = temp_screen
        self.pipe_type: str = pipe_type
        self.top_pipe: Surface = pygame.image.load("./img/" + self.pipe_type + "_down.png")
        self.bottom_pipe: Surface = pygame.image.load("./img/" + self.pipe_type + "_up.png")
        self.top_pipe: Surface = pygame.transform.smoothscale(self.top_pipe, (self.top_pipe.get_width(), 512 // 5 * 4))
        self.bottom_pipe: Surface = pygame.transform.smoothscale(self.bottom_pipe,
                                                                 (self.bottom_pipe.get_width(), 512 // 5 * 4))
        self.isCrash = True
        self.middle_long = self.screen.get_height() // 4
        self.top_long = random.randint(0, self.middle_long * 2)
        self.top_x = self.screen.get_width()
        self.bottom_x = self.screen.get_width()
        self.top_y = self.top_long - self.top_pipe.get_height()
        self.bottom_y = self.top_long + self.middle_long
        self.top_rect = pygame.Rect(self.top_x, self.top_y, self.top_pipe.get_width(), self.top_pipe.get_height())
        self.bottom_rect = pygame.Rect(self.bottom_x, self.bottom_y, self.bottom_pipe.get_width(),
                                       self.bottom_pipe.get_height())

    def display(self):
        self.screen.blit(self.top_pipe, (self.top_x, self.top_y))
        self.screen.blit(self.bottom_pipe, (self.bottom_x, self.bottom_y))
        self.top_rect = pygame.Rect(self.top_x, self.top_y, self.top_pipe.get_width(), self.top_pipe.get_height())
        self.bottom_rect = pygame.Rect(self.bottom_x, self.bottom_y, self.bottom_pipe.get_width(), self.bottom_pipe.get_height())
        # 显示碰撞体
        # pygame.draw.rect(self.screen, (255, 0, 0), self.top_rect, 2)
        # pygame.draw.rect(self.screen, (255, 0, 0), self.bottom_rect, 2)

    def move(self):
        self.top_x -= 10
        self.bottom_x -= 10
