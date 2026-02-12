import pygame
import sys
from settings import *
from maze import Maze
from pacman import Pacman
from ghost import Ghost

# 初始化 Pygame
pygame.init()

# 设置窗口
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("吃豆人游戏")

#设置帧率
clock = pygame.time.Clock()

maze=Maze()

pacman=Pacman(10*CELL_SIZE+CELL_SIZE//2,16*CELL_SIZE+CELL_SIZE//2)

ghosts=[
    Ghost(9.5*CELL_SIZE,9.5*CELL_SIZE,RED,"Blinky"),
    Ghost(10.5*CELL_SIZE,9.5*CELL_SIZE,PINK,"Pinky"),
    Ghost(9.5*CELL_SIZE,10.5*CELL_SIZE,CYAN,"Inky"),
    Ghost(10.5*CELL_SIZE,10.5*CELL_SIZE,ORANGE,"Clyde")
]

score=0
font=pygame.font.Font(None,36)

def check_collision(pacman,ghost):
    """检查吃豆人和幽灵是否碰撞"""
    dx=pacman.x-ghost.x
    dy=pacman.y-ghost.y
    distance=(dx**2+dy**2)**0.5
    #如果距离小于两个半径之和,就是碰撞
    return distance<(pacman.radius+ghost.radius)

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

# 游戏主循环
running = True
while running:
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #处理输入
    pacman.handle_input()

    earned_score,is_power_pellet=pacman.move(maze)
    score+=earned_score

    if is_power_pellet:
        for ghost in ghosts:
            ghost.state="frightened"
            ghost.frightened_timer=600 #持续10秒

    #更新幽灵恐惧计时器
    for ghost in ghosts:
        if ghost.frightened_timer>0 and ghost.state!="eaten":
            ghost.frightened_timer-=1
            if ghost.frightened_timer==0:
                ghost.state="normal"

    for ghost in ghosts:
        print(f"{ghost.name}: x={ghost.x}, y={ghost.y}")
        ghost.move(maze)

        if check_collision(pacman,ghost):
            if ghost.state=="frightened":
                #吃掉幽灵,加分
                score+=200
                ghost.state="eaten"
                ghost.x=1000
                ghost.y=1000
            else:
                #游戏结束
                print("Game Over!")
                running=False
    #更新游戏状态
    remaining_dots=maze.count_remaining_dots()


    # 填充背景色
    screen.fill(BLACK)

    #绘制迷宫
    maze.draw(screen)
    pacman.draw(screen)

    for ghost in ghosts:
        ghost.draw(screen)
    
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