import pygame
import sys
from settings import *
from maze import Maze

# 初始化 Pygame
pygame.init()

# 设置窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("吃豆人游戏")

#设置帧率
clock = pygame.time.Clock()

maze=Maze()

# 游戏主循环
running = True
while running:
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 填充背景色
    screen.fill(BLACK)

    #绘制迷宫
    maze.draw(screen)

    # 更新显示
    pygame.display.flip()
    
    # 控制帧率
    clock.tick(FPS)

# 退出游戏
pygame.quit()
sys.exit()