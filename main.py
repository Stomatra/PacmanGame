import pygame
import sys
from settings import *
from maze import Maze
from pacman import Pacman

# 初始化 Pygame
pygame.init()

# 设置窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("吃豆人游戏")

#设置帧率
clock = pygame.time.Clock()

maze=Maze()

pacman=Pacman(10*CELL_SIZE+CELL_SIZE//2,16*CELL_SIZE+CELL_SIZE//2)

score=0
font=pygame.font.Font(None,36)

# 游戏主循环
running = True
while running:
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #处理输入
    pacman.handle_input()
    earned_score=pacman.move(maze)
    score+=earned_score

    #更新游戏状态
    pacman.move(maze)
    remaining_dots=maze.count_remaining_dots()

    def draw_score_and_count_remaining_dots(screen,score):
        """在屏幕上显示分数和剩余豆子"""
        text=font.render(f"score:{score},remaining dots:{remaining_dots}",True,WHITE)
        screen.blit(text,(10,10))

    def draw_win_screen(screen):
        """显示胜利画面"""
        win_font=pygame.font.Font(None,72)
        win_text=win_font.render("YOU WIN!",True,YELLOW)
        text_rect=win_text.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
        screen.blit(win_text,text_rect)

    # 填充背景色
    screen.fill(BLACK)

    #绘制迷宫
    maze.draw(screen)
    pacman.draw(screen)
    
    draw_score_and_count_remaining_dots(screen,score)

    if remaining_dots==0:
        draw_win_screen(screen)
        
    # 更新显示
    pygame.display.flip()
    
    # 控制帧率
    clock.tick(FPS)

# 退出游戏
pygame.quit()
sys.exit()