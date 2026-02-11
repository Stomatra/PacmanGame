import pygame
from settings import *

class Maze:
    def __init__(self):
        self.layout=MAZE
    def draw(self,screen):
        index=0
        for i in MAZE:#i为行
            for j in i:#j为列
                #- `0` = 空白通道（吃豆人可以走）
                #- `1` = 墙壁（蓝色方块）
                #- `2` = 小豆子（可以吃）
                #- `3` = 大豆子/能量豆（吃了可以反击幽灵）
                grid=pygame.Rect(GRID_WIDTH*(index%22),GRID_HEIGHT*(index//22),GRID_WIDTH,GRID_HEIGHT)
                if j==0:
                    pass
                elif j==1:
                    pygame.draw.rect(screen,(0,0,255),grid)
                elif j==2:
                    pygame.draw.rect(screen,(255,255,0),grid)
                elif j==3:
                    pygame.draw.rect(screen,(0,255,0),grid)
                index+=1
