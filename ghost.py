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
        self.radius=CELL_SIZE//2-1

        self.state="normal"#normal/frightened/eaten
        self.frightened_timer=0 #恐惧模式剩余时间

    def move(self,maze):
        """简单随机移动"""
        if self._should_change_direction(maze):
            self._choose_direction(maze)

        new_x,new_y=self._calculate_next_position()

        if not self._will_collide(new_x,new_y,maze):
            self.x=new_x
            self.y=new_y

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
        
        if self._is_near_grid_center() and self._is_at_intersection(maze):
            return random.random()<0.1
        
        return False

    def _is_near_grid_center(self):
        """检查是否接近格子中心"""
        offset_x=self.x%CELL_SIZE
        offset_y=self.y%CELL_SIZE

        center=CELL_SIZE/2
        threshold=2
        
        #如果x和y都接近格子中心
        near_x=abs(offset_x-center)<threshold
        near_y=abs(offset_y-center)<threshold

        return near_x and near_y

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

        #找出所有可行方向
        for direction in [UP,DOWN,LEFT,RIGHT]:
            test_x,test_y=self._get_next_position(direction)
            if not self._will_collide(test_x,test_y,maze):
                possible_directions.append(direction)

        if not possible_directions:
            print(f"{self.name}无路可走！")
            return
        
        #获取反方向
        reverse_direction=self._get_reverse_direction(self.direction)

        #过滤掉反方向（除非只有反方向可走）
        forward_directions=[d for d in possible_directions if d!=reverse_direction]
            
        #优先选择非反向的方向
        if possible_directions:
            self.direction=random.choice(forward_directions)

    def _get_reverse_direction(self,direction):
        """获取反方向"""
        if direction==UP:
            return DOWN
        elif direction==DOWN:
            return UP
        elif direction==LEFT:
            return RIGHT
        elif direction==RIGHT:
            return LEFT
        else:
            return STAND

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