'''
  Copyright (C) Ana Belen Sarabia Cobo <belensarabia@gmail.com>

  This program is free software; you can redistribute it and/or 
  modify it under the terms of the GNU General Public License
  Version 3 as published by the Free Software Foundation
  
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 51 Franklin Street, Fifth Floor,
  Boston, MA 02110-1301, USA.
'''


from vector import ZERO2, Vector2
import entity
from physics import Rect, Body
from game_config import WINDOW_WIDTH, WINDOW_HEIGHT, BALL_WIDTH, BALL_HEIGHT, PADDLE_WIDTH,\
                        PADDLE_HEIGHT, WALL_WIDTH, WALL_HEIGHT,\
                        BRICK_WIDTH, BRICK_HEIGHT, BRICK_SPACING, BRICKS_COLORS


class Map(object):   
    def __init__(self):
        # Entities
        self.balls = []
        self.bricks = []
        self.paddles = []

        # Other bodies
        self.bodies = []  
                  
        ball_position = Vector2((WINDOW_WIDTH - BALL_WIDTH) * 0.5, 
                                WINDOW_HEIGHT - PADDLE_HEIGHT - BALL_HEIGHT)      
        self.balls.append(entity.DefaultBall(ball_position.x, ball_position.y))
        
        paddle_position = Vector2((WINDOW_WIDTH - PADDLE_WIDTH) * 0.5, 
                                  WINDOW_HEIGHT - PADDLE_HEIGHT)       
        self.paddles.append(entity.DefaultPaddle(paddle_position.x, paddle_position.y))    
        
        # Create bodies enclosing the game screen area

        top_rect = Rect(Vector2(0.0, -WALL_HEIGHT), WINDOW_WIDTH, WALL_HEIGHT)
        bottom_rect = Rect(Vector2(0.0, WINDOW_HEIGHT), WINDOW_WIDTH, WALL_HEIGHT)
        left_rect = Rect(Vector2(-WALL_WIDTH, -WALL_HEIGHT), WALL_WIDTH, WINDOW_HEIGHT + 2 * WALL_HEIGHT)
        right_rect = Rect(Vector2(WINDOW_WIDTH, -WALL_HEIGHT), WALL_WIDTH, WINDOW_HEIGHT + 2 * WALL_HEIGHT)
        
        self.bodies.append(Body(top_rect, ZERO2, 'top-wall', True))
        self.bodies.append(Body(bottom_rect, ZERO2, 'bottom-wall', True))
        self.bodies.append(Body(left_rect, ZERO2, 'left-wall', True))
        self.bodies.append(Body(right_rect, ZERO2, 'right-wall', True))


class MapOne(Map):
    def __init__(self):
        BRICK_COUNT_X = 11
        BRICK_COUNT_Y = 6        
        super(MapOne, self).__init__()       
        start_position = Vector2((WINDOW_WIDTH - (BRICK_COUNT_X * BRICK_WIDTH + (BRICK_COUNT_X - 1) * BRICK_SPACING) ) * 0.5, 
                                  WINDOW_HEIGHT * 0.5)        
        for y in range(BRICK_COUNT_Y):
            brick_color = BRICKS_COLORS[y % len(BRICKS_COLORS)]
            for x in range(BRICK_COUNT_X):
                if brick_color != 'grey':
                    self.bricks.append(entity.DefaultBrick(start_position.x + x * (BRICK_WIDTH + BRICK_SPACING),
                                                           start_position.y - y * (BRICK_HEIGHT + BRICK_SPACING),
                                                           brick_color))
                else:
                    self.bricks.append(entity.MultiHit(start_position.x + x * (BRICK_WIDTH + BRICK_SPACING),
                                                       start_position.y - y * (BRICK_HEIGHT + BRICK_SPACING),
                                                       brick_color))
                    
                    
class MapTwo(Map):
    def __init__(self):
        BRICK_COUNT_X = 11     
        super(MapTwo, self).__init__()
        
        start_position = Vector2((WINDOW_WIDTH - (BRICK_COUNT_X * BRICK_WIDTH + (BRICK_COUNT_X - 1) * BRICK_SPACING) ) * 0.5, 
                                  WINDOW_HEIGHT * 0.5)
        b_c = BRICKS_COLORS[:]
        b_c.remove('grey')
        for x in range(BRICK_COUNT_X):
            brick_color = b_c[x % len(b_c)]
            for y in range(BRICK_COUNT_X - x):
                self.bricks.append(entity.DefaultBrick(start_position.x + x * (BRICK_WIDTH + BRICK_SPACING),
                                                       start_position.y - y * (BRICK_HEIGHT + BRICK_SPACING),
                                                       brick_color))                
        for x in range(BRICK_COUNT_X):
            self.bricks.append(entity.MultiHit(start_position.x + x * (BRICK_WIDTH + BRICK_SPACING),
                               start_position.y +  (BRICK_HEIGHT + BRICK_SPACING),
                               'grey'))
            

class MapSelector():
    map_types = [MapOne, MapTwo]

    def __init__(self):
        self.current_map = -1
        
    def initialize_current_map(self):
        self.current_map = -1
        
    def get_next_map(self):
        self.current_map = self.current_map + 1
        return self.map_types[self.current_map]()
       
    def has_next_map(self):
        if self.current_map + 1 < len(self.map_types):
            return True  
        return False
