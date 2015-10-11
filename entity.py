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

import pygame


from physics import Body, Rect
from vector import ZERO2, Vector2
from graphics import Graphics
from game_config import BRICK_WIDTH, BRICK_HEIGHT, BRICK_NUMBER, BRICKS_COLORS, BALL_WIDTH,\
                        BALL_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT, IMAGE_FILE_NAME


graphics = Graphics()  


class Entity(object):
    """
    Represents the entities of the game, which are game objects with a graphics and a physics representation
    """
    def __init__(self, body, surface, surface_src):
        self.body = body
        self.surface = surface 
        self.surface_src = surface_src 


class Brick(Entity):
    def __init__(self, body, surface, surface_src, health_points=1):
        super(Brick, self).__init__(body, surface, surface_src)
        self.health_points = health_points 
        
    def apply_damage(self, damage_points=1):
        self.health_points = max(0, self.health_points - damage_points)


class DefaultBrick(Brick):  
    def __init__(self, x, y, brick_color, health_points=1):           
        surface_src_b = None
        for i, color in enumerate(BRICKS_COLORS): 
            if color == brick_color:     
                surface_src_b = pygame.Rect(0, BRICK_HEIGHT * i, BRICK_WIDTH, BRICK_HEIGHT)
                break
        super(DefaultBrick, self).__init__(Body(Rect(Vector2(x, y), 
                                                     BRICK_WIDTH, 
                                                     BRICK_HEIGHT),
                                                ZERO2,
                                                'brick',
                                                self, # general purpose tag references the body's owner entity
                                                True),
                                           graphics.get_image(IMAGE_FILE_NAME), 
                                           surface_src_b, health_points)


class MultiHit(DefaultBrick):   
    def __init__(self, x, y, color, health_points=2):           
        super(MultiHit, self).__init__(x, y, color, health_points)

    def apply_damage(self, damage_points=1):
        self.health_points = max(0, self.health_points - damage_points)    
        if self.health_points == 1:  
            self.surface_src.top = self.surface_src.top + BRICK_HEIGHT


class Ball(Entity):
    def __init__(self, body, surface, surface_src, damage_points=1):
        super(Ball, self).__init__(body, surface, surface_src)
        self.damage_points = damage_points 


class DefaultBall(Ball):
    """
    Default ball is initialized as a static entity
    """
    def __init__(self, x, y, damage_points=1):
        super(DefaultBall, self).__init__(Body(Rect(Vector2(x, y),
                                                    BALL_WIDTH, 
                                                    BALL_HEIGHT),
                                               ZERO2,
                                               'ball',
                                               self, # general purpose tag references the body's owner entity
                                               True),
                                          graphics.get_image(IMAGE_FILE_NAME),
                                          pygame.Rect(0, (BRICK_NUMBER * BRICK_HEIGHT) + PADDLE_HEIGHT, 
                                                          BALL_WIDTH, 
                                                          BALL_HEIGHT)) 
        self.damage_points = damage_points 
 
    
class Paddle(Entity):
    def __init__(self, body, surface, surface_src):
        super(Paddle, self).__init__(body, surface, surface_src)

        
class DefaultPaddle(Paddle):
    def __init__(self, x, y):
        super(DefaultPaddle, self).__init__(Body(Rect(Vector2(x, y), 
                                                      PADDLE_WIDTH, 
                                                      PADDLE_HEIGHT),
                                                 ZERO2,
                                                 'paddle',
                                                 self,
                                                 True),
                                            graphics.get_image(IMAGE_FILE_NAME), 
                                            pygame.Rect(0, BRICK_NUMBER * BRICK_HEIGHT, 
                                                        PADDLE_WIDTH, 
                                                        PADDLE_HEIGHT))        
