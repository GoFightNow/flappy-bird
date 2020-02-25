# Created by Go_Fight_Now on 2019/12/8 15:49. #
# -*- coding:utf-8 -*-
import pygame, random
from pygame import Surface


class MyBird:
    def __init__(self, temp_screen: Surface) -> None:
        self.screen = temp_screen

        self.bird_type = random.choice(['bird0', 'bird1', 'bird2'])
        self.bird_img = [pygame.image.load("./img/"+self.bird_type+"_0.png"), pygame.image.load("./img/"+self.bird_type+"_1.png"),
                         pygame.image.load("./img/"+self.bird_type+"_2.png")]
        self.bird_index = 0
        self.bird: Surface = pygame.transform.rotate(self.bird_img[self.bird_index], 0)
        self.x = self.screen.get_width() // 10
        self.y = (self.screen.get_height() - self.bird.get_height()) // 2
        self.rect = pygame.Rect(self.x, self.y, self.bird.get_width(), self.bird.get_height())
        self.isBottom = False
        self.head_angle = [i for i in range(45, -46, -1) if i % 5 == 0]
        self.head_index = 0
        self.down_speed = [float(str(i) + '.' + str(j)) for i in range(4) for j in range(10)]
        self.down_speed.append(4.0)
        self.down_index = 0
        self.score = 0

    def update(self):
        # 鸟的图片
        if self.bird_index < 2:
            self.bird_index += 1
        else:
            self.bird_index = 0
        # 计算鸟头的角度
        if self.head_angle[self.head_index] > self.head_angle[len(self.head_angle) - 1]:
            self.head_index += 1
        else:
            self.head_index = len(self.head_angle) - 1
        # 显示鸟
        self.bird: Surface = pygame.transform.rotate(self.bird_img[self.bird_index], self.head_angle[self.head_index])
        self.rect = pygame.Rect(self.x, self.y, 24, 24)
        self.rect.center = ((self.bird.get_width() + self.x * 2) // 2, (self.bird.get_height() + self.y * 2) // 2)

    def display(self):
        self.screen.blit(self.bird, (self.x, self.y))

        # 显示碰撞体积
        # pygame.draw.rect(self.screen, (255, 0, 0), self.rect, 2)

    def scope(self):
        if self.rect.top <= 0:
            self.y = 48 - self.bird.get_height()
            return -1
        elif self.y + self.bird.get_height() >= self.screen.get_height():
            self.isBottom = True
            self.y = self.screen.get_height() - self.bird.get_height() + self.rect.height
            return -1

    def move_down(self):
        self.y += self.down_speed[self.down_index]
        if self.down_speed[self.down_index] < 4:
            self.down_index += 1
        else:
            self.down_index = len(self.down_speed) - 1

    def move_up(self):
        self.isBottom = False
        self.down_index = 0
        self.head_index = 0
        self.y -= 50
