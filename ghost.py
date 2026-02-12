import pygame
from settings import *
import random

class Ghost:
    def __init__(self,x,y,color,name):
        self.x=x
        self.y=y
        self.color=color
        self.name=name
        self.speed=GHOST_SPEED
        self.direction=UP
        self.radius=CELL_SIZE//2-2

        self.state="normal"#normal/frightened/eaten
        self.frightened_timer=0 #恐惧模式剩余时间

    def move(self,maze):
        """简单随机移动"""
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

        if self._will_collide(new_x,new_y,maze) or self._is_at_intersection(maze):
            self._choose_direction(maze)
        else:
            self.x=new_x
            self.y=new_y

        if self._will_collide(new_x, new_y, maze):
            print(f"{self.name} 撞墙了，尝试换方向")
            self._choose_direction(maze)

    def draw(self,screen):
        """绘制幽灵"""
        # 根据状态选择颜色
        if self.state=="frightened":
            color=BLUE
        else:
            color=self.color

        pygame.draw.circle(screen,color,(int(self.x),int(self.y)),self.radius)

    def _should_change_direction(self,maze):
        """判断是否需要换方向"""
        new_x,new_y=self._calculate_next_position()

        if self._will_collide(new_x,new_y,maze):
            return True
        
        if self._is_at_intersection(maze):
            return random.random()<0.2
        
        return False

    def _calculate_next_position(self):
        """根据当前方向计算下一个位置"""
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

        return new_x,new_y

    def _choose_direction(self,maze):
        """选择一个可行的方向"""
        possible_directions=[]

        for direction in [UP,DOWN,LEFT,RIGHT]:
            test_x,test_y=self._get_next_position(direction)
            if not self._will_collide(test_x,test_y,maze):
                possible_directions.append(direction)
            
        if possible_directions:
            self.direction=random.choice(possible_directions)

    def _get_next_position(self,direction):
        """根据方向计算下一个位置"""
        x,y=self.x,self.y
        if direction==LEFT:
            x-=self.speed
        elif direction==RIGHT:
            x+=self.speed
        elif direction==UP:
            y-=self.speed
        elif direction==DOWN:
            y+=self.speed
        return x,y
    
    def _is_at_intersection(self,maze):
        """检查是否在路口"""
        #检查上下左右是否有多于两个方向可走
        count=0
        for direction in [UP,DOWN,LEFT,RIGHT]:
            test_x,test_y=self._get_next_position(direction)
            if not self._will_collide(test_x,test_y,maze):
                count+=1

        return count>=3 #三个或更多路口
    
    def _will_collide(self,x,y,maze):
        """检查是否会撞墙(方形碰撞箱)"""
        box_size=self.radius*0.85

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