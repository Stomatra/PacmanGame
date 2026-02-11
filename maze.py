import pygame
from settings import *

class Maze:
    def __init__(self):
        self.layout=MAZE

    def draw(self,screen):
        """绘制迷宫"""
        for row in range(len(self.layout)):
            for col in range(len(self.layout[row])):
                x=col*CELL_SIZE
                y=row*CELL_SIZE

                cell_value=self.layout[row][col]

                if cell_value==WALL:
                    pygame.draw.rect(screen,BLUE,(x,y,CELL_SIZE,CELL_SIZE))

                elif cell_value==CELL:
                    center_x=x+CELL_SIZE//2
                    center_y=y+CELL_SIZE//2
                    pygame.draw.circle(screen,WHITE,(center_x,center_y),3)

                elif cell_value==BIG_CELL:
                    center_x=x+CELL_SIZE//2
                    center_y=y+CELL_SIZE//2
                    pygame.draw.circle(screen,GREEN,(center_x,center_y),8)

    def is_wall(self,x,y):
        """检查是否是墙壁"""
        grid_x=x//CELL_SIZE
        grid_y=y//CELL_SIZE

        if grid_y<0 or grid_y>=len(self.layout):
            return True
        if grid_x<0 or grid_x>=len(self.layout[0]):
            return True
        
        return self.layout[grid_y][grid_x]==1

    def eat_dot(self,x,y):
        grid_x=x//CELL_SIZE
        grid_y=y//CELL_SIZE
        
        if grid_y<0 or grid_y>=len(self.layout):
            return 0
        if grid_x<0 or grid_x>=len(self.layout[0]):
            return 0
        
        cell_value=self.layout[grid_y][grid_x]

        if cell_value==CELL:
            self.layout[grid_y][grid_x]=0
            return 10
        elif cell_value==BIG_CELL:
            self.layout[grid_y][grid_x]=0
            return 50
        
        return 0
    
    def count_remaining_dots(self):
        """统计地图上还有多少豆子,用来判断是否胜利"""
        count=0
        for row in self.layout:
            for cell in row:
                if cell==CELL or cell==BIG_CELL:
                    count+=1

        return count 
