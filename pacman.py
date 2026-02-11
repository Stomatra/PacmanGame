import pygame
import math
from settings import *

class Pacman:
    def __init__(self, x, y):
        # 初始化位置、方向、速度
        self.x=x
        self.y=y

        self.speed=PACMAN_SPEED

        #0,1,2,3,4分别表示静止,上,下,左,右
        self.direction=STAND

        #缓冲方向
        self.next_direction=STAND

        self.radius = CELL_SIZE // 2 -1
    
    def handle_input(self):
        # 处理键盘输入，存储到缓冲方向
        keys=pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.next_direction=LEFT
        elif keys[pygame.K_RIGHT]:
            self.next_direction=RIGHT
        elif keys[pygame.K_UP]:
            self.next_direction=UP
        elif keys[pygame.K_DOWN]:
            self.next_direction=DOWN
        elif keys[pygame.K_SPACE]:
            self.next_direction=STAND

    def move(self, maze):
        # 移动，并检测是否撞墙
        if self.next_direction!=STAND:
            test_x=self.x
            test_y=self.y

            if self.next_direction==LEFT:
                test_x-=self.speed
            elif self.next_direction==RIGHT:
                test_x+=self.speed
            elif self.next_direction==UP:
                test_y-=self.speed
            elif self.next_direction==DOWN:
                test_y+=self.speed

            if not self._will_collide(test_x,test_y,maze):
                self.direction=self.next_direction
                self.next_direction=STAND

        new_x=self.x
        new_y=self.y
        if self.direction==LEFT:
            new_x-=self.speed
        elif self.direction==RIGHT:
            new_x+=self.speed
        elif self.direction==UP:
            new_y-=self.speed
        elif self.direction==DOWN:
            new_y+=self.speed

        if not self._will_collide(new_x,new_y,maze):
            self.x=new_x
            self.y=new_y
            
            score=maze.eat_dot(self.x,self.y)
            return score
        else:
            self.direction=STAND
            return 0

    def _will_collide(self, x, y, maze):
        """使用方形碰撞箱检测"""
        # 定义碰撞箱大小(比圆形略小,避免卡墙)
        box_size=self.radius

        corners=[
            (x-box_size,y-box_size),
            (x+box_size,y-box_size),
            (x-box_size,y+box_size),
            (x+box_size,y+box_size)
        ]

        for corner_x,corner_y in corners:
            if maze.is_wall(int(corner_x),int(corner_y)):
                return True
            
        return False
    
    def draw(self, screen):
        # 画一个黄色圆形（简化版）
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)