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
import time
import math


from game_config import TITLE_COLOR, BLACK, BLUE, FONT_SIZE_BASIC, FONT_SIZE_BIG, TEXT_LINE_SPACING,\
                        WINDOW_WIDTH, WINDOW_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_VELOCITY,\
                        PADDLE_LINE_SPACING,BALL_WIDTH, BALL_HEIGHT, BALL_VELOCITY_Y, BALL_VELOCITY_X,\
                        BALL_PUSH, STEP_TIME, MAX_FPS, STEP_TIME_INTEGRATE           
from graphics import Graphics
import utils
import inputs
import physics
from map import MapSelector
from vector import ZERO2, Vector2, normalize, magnitude, sum, dot, mul, rotate


graphics = Graphics() 


class InitLayer:
    """
    Shows the initial game menu   
    """     
    def __init__(self, owner):
        self.owner = owner
        self.text_menu = 'MENU: '
        self.text_enter = 'Press ENTER to play '   
        self.text_esc = 'Press ESC to exit'
        self.fps_clock = pygame.time.Clock()
        
    def initialize(self, previous_layer):         
        self.title_surf_menu, self.title_rect_menu = graphics.make_text_obj(self.text_menu, 
                                                                           TITLE_COLOR,
                                                                           FONT_SIZE_BASIC)
        self.title_surf_enter, self.title_rect_enter = graphics.make_text_obj(self.text_enter, 
                                                                             TITLE_COLOR, 
                                                                             FONT_SIZE_BASIC)
        self.title_surf_esc, self.title_rect_esc = graphics.make_text_obj(self.text_esc, 
                                                                         TITLE_COLOR, 
                                                                         FONT_SIZE_BASIC) 

        self.title_rect_menu.left = (WINDOW_WIDTH - self.title_rect_menu.width) / 2
        self.title_rect_enter.left = (WINDOW_WIDTH - self.title_rect_enter.width) / 2
        self.title_rect_esc.left = (WINDOW_WIDTH - self.title_rect_esc.width) / 2
        
        text_block_height = self.title_rect_menu.height + self.title_rect_enter.height + self.title_rect_esc.height + \
            2 * TEXT_LINE_SPACING

        self.title_rect_menu.top = (WINDOW_HEIGHT - text_block_height) / 2
        self.title_rect_enter.top = self.title_rect_menu.top + TEXT_LINE_SPACING
        self.title_rect_esc.top =  self.title_rect_enter.top + TEXT_LINE_SPACING 
        
    def run(self):
        """
        Waits for the user to either press the exit key or any other key to start the game       
        """
        while not inputs.is_key_pressed(): 
            graphics.clear_display_surf(BLACK)
            graphics.get_display_surf().blit(self.title_surf_menu, self.title_rect_menu)
            graphics.get_display_surf().blit(self.title_surf_enter, self.title_rect_enter)
            graphics.get_display_surf().blit(self.title_surf_esc, self.title_rect_esc)
            graphics.flip_display_surf()
            self.fps_clock.tick(4)
        inputs.clear_event_queue()

    def at_exit(self):
        self.owner.set_layer(self.owner.GAME_LAYER)


class GameLayer:
    """
    Processes the main game logic
    """   
    INITIALIZATION = 0
    GAME_LOOP = 1
    GAME_EXIT = 2
    GAME_WIN_SCREEN = 3
    GAME_PAUSE_SCREEN = 4
    
    def __init__(self, owner):
        self.owner = owner        
        self.moving_right = False
        self.moving_left = False        
        self.push_balls = False 
               
        self.fps_clock = pygame.time.Clock() 
           
        self.physics_world = physics.PhysicsWorld(STEP_TIME_INTEGRATE) 
        
        self.game_status = GameLayer.INITIALIZATION       
        self.current_map = MapSelector()
        
        self.bricks = []
        self.paddles = []
        self.balls = []

        self.entities = []
        self.bodies = []       
        
        on_ball_brick_event = self.physics_world.CallBack('ball', 'brick', self.on_ball_brick_collision)
        on_ball_paddle_event = self.physics_world.CallBack('ball', 'paddle', self.on_ball_paddle_collision)
        on_ball_bottom_wall_event = self.physics_world.CallBack('ball', 'bottom-wall', self.on_ball_bottom_wall_collision)
        on_ball_left_wall_event = self.physics_world.CallBack('ball', 'left-wall', self.on_ball_left_right_collision)
        on_ball_right_wall_event = self.physics_world.CallBack('ball', 'right-wall', self.on_ball_left_right_collision)
        
        
        self.physics_world.add_callback(on_ball_brick_event)
        self.physics_world.add_callback(on_ball_paddle_event)
        self.physics_world.add_callback(on_ball_bottom_wall_event) 
        self.physics_world.add_callback(on_ball_left_wall_event)
        self.physics_world.add_callback(on_ball_right_wall_event)     
        
    def initialize(self, previous_layer):      
        self.moving_right = False
        self.moving_left = False           
        self.push_balls = False
        
        self.game_status = GameLayer.INITIALIZATION            
        self.current_map.initialize_current_map()
        self.update_map()
        
    def clear_game(self):
        self.bricks = []
        self.paddles = []
        self.balls = []

        self.entities = []
        self.bodies = []
        
        self.physics_world.clear_bodies()
        
        self.push_balls = False
    
    def update_map(self):
        self.clear_game()
        m = self.current_map.get_next_map()
        
        for brick in m.bricks:
            self.register_entity(brick)
            self.bricks.append(brick)

        for ball in m.balls:
            self.register_entity(ball)
            self.balls.append(ball)

        for paddle in m.paddles:
            self.register_entity(paddle)
            self.paddles.append(paddle)

        for body in m.bodies:
            self.register_body(body)

    def register_body(self, new_body):
        if not new_body in self.bodies:
            self.physics_world.add_body(new_body)
            self.bodies.append(new_body)

    def register_entity(self, new_entity):
        if not new_entity in self.entities:
            self.physics_world.add_body(new_entity.body)
            self.entities.append(new_entity) 

    def unregister_entity(self, entity):
        if entity in self.entities:
            self.physics_world.delete_body(entity.body)
            self.entities.remove(entity)                              

    def on_ball_brick_collision(self, ball_body, brick_body, normal):       
        brick_ent = brick_body.tag_ent
        ball_ent = ball_body.tag_ent
        brick_ent.apply_damage(ball_ent.damage_points) 
        ball_ent.body.set_velocity(min(self.physics_world.MAX_SPEED, ball_body.velocity * 1.1)) 
        
    def on_ball_paddle_collision(self, ball_body, paddle_body, normal):
        # Adjusts the ball direction if the paddle is moving when the ball collides with it
        angle = math.acos(dot(normal, ball_body.direction)) # Angle between the reflected direction and the normal
        delta_angle = abs(((math.pi * 0.5) - angle) * 0.5) # Half the angle that remains if were to perform a 90 degree reflection
        if paddle_body.direction.x > 0: # Clockwise rotation because the paddle is moving to the right
            ball_body.direction = normalize(rotate(ball_body.direction, delta_angle))
        elif paddle_body.direction.x < 0: # Counter-clockwise rotation because the paddle is moving to the left
            ball_body.direction = normalize(rotate(ball_body.direction, -delta_angle))           
                   
    def on_ball_bottom_wall_collision(self, bottom_body, ball_body, normal):
        if len(self.balls) == 1:
            self.game_status = GameLayer.GAME_EXIT     
        else:
            ball_ent = ball_body.tag_ent
            self.unregister_entity(ball_ent)
    
    def on_ball_left_right_collision(self, ball_body, wall_body, normal):
        angle = math.acos(dot(normal, ball_body.direction)) # Angle between the reflected direction and the normal

        # If the angle is too flat, add a small rotation to the reflected direction
        if angle < 0.1:
            delta_angle = 0.2
            if ball_body.direction.y > 0: # Counter-clockwise rotation because the ball is moving downwards
                ball_body.direction = normalize(rotate(ball_body.direction, -delta_angle))
            elif ball_body.direction.y <= 0: # Clockwise rotation because the ball is moving upwards 
                ball_body.direction = normalize(rotate(ball_body.direction, delta_angle))   
            
    def update(self, step_time):
        def change_dir_vel(entities, direction, velocity):
            for entity in entities:
                entity.body.direction = direction
                entity.body.set_velocity(velocity)
           
        if(self.moving_left or self.moving_right):
            if self.moving_left:
                change_dir_vel(self.paddles, Vector2(-1,0), PADDLE_VELOCITY)
                if self.game_status == GameLayer.INITIALIZATION:
                    change_dir_vel(self.balls, Vector2(-1,0), PADDLE_VELOCITY)  
            else:
                change_dir_vel(self.paddles, Vector2(1,0), PADDLE_VELOCITY)
                if self.game_status == GameLayer.INITIALIZATION:
                    change_dir_vel(self.balls, Vector2(1,0), PADDLE_VELOCITY)    
        else:
            change_dir_vel(self.paddles, ZERO2, magnitude(ZERO2))
            if self.game_status == GameLayer.INITIALIZATION:
                change_dir_vel(self.balls, ZERO2, magnitude(ZERO2))
                    
        if self.push_balls and self.game_status == GameLayer.INITIALIZATION:                  
            for ball in self.balls:
                if ball.body.is_static:
                    ball.body.is_static = False
            v = Vector2(BALL_VELOCITY_X, BALL_VELOCITY_Y) 
            change_dir_vel(self.balls, normalize(v), magnitude(v))
            self.push_balls = False
            self.game_status = GameLayer.GAME_LOOP
             
        # Remove bricks that have been destroyed
        free_brick_list = []
        for brick in self.bricks:
            if brick.health_points == 0:
                self.unregister_entity(brick)
                free_brick_list.append(brick)
        self.bricks = [ b for b in self.bricks if free_brick_list.count(b) == 0 ] 
                
        for paddle in self.paddles:          
            # Integrate paddle
            paddle.body.rect.position = sum(paddle.body.rect.position,
                                            mul(paddle.body.direction, paddle.body.velocity * step_time))
    
            # Relocate paddle position to a valid position range
            paddle.body.rect.position.x = utils.clamp(paddle.body.rect.position.x, 0, 
                                                      WINDOW_WIDTH - PADDLE_WIDTH)
            paddle.body.rect.position.y = WINDOW_HEIGHT - PADDLE_HEIGHT - PADDLE_LINE_SPACING

        for ball in self.balls:
            if ball.body.is_static:
                pos_r = Vector2((PADDLE_WIDTH - BALL_WIDTH) * 0.5,  - BALL_HEIGHT)
                ball.body.rect.position = sum(self.paddles[0].body.rect.position, pos_r)
     
    def run(self):
        """
        Main game loop: processes inputs, updates the game status and renders the game scene
        """        
        last_update_time = pygame.time.get_ticks()
        accumulated = 0.0
        while self.game_status == GameLayer.INITIALIZATION or self.game_status == GameLayer.GAME_LOOP:
            #Process inputs       
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    utils.terminate()             
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.moving_left = True
                    elif event.key == pygame.K_RIGHT:
                        self.moving_right = True
                    elif event.key == pygame.K_a:
                        self.push_balls = True 
                    elif event.key == pygame.K_p: 
                        self.game_status = GameLayer.GAME_PAUSE_SCREEN
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        utils.terminate()
                    elif event.key == pygame.K_RIGHT:
                        self.moving_right = False
                    elif event.key == pygame.K_LEFT:
                        self.moving_left = False  
                  
            time = pygame.time.get_ticks()    
            delta_time = time - last_update_time
            
            accumulated = accumulated + delta_time                
            if accumulated > BALL_PUSH: 
                self.push_balls = True
                accumulated = 0.0
            
            while delta_time > 0:
                sim_step_time = STEP_TIME
                if delta_time - STEP_TIME < 0:
                    sim_step_time = delta_time
                self.update(sim_step_time)
                self.physics_world.step_simulation(sim_step_time)
                
                if len(self.bricks) < 1:
                    if not self.current_map.has_next_map():
                        self.game_status = GameLayer.GAME_WIN_SCREEN
                    else:
                        self.update_map()
                        self.game_status = GameLayer.INITIALIZATION
                        accumulated = 0
                delta_time -= sim_step_time
            last_update_time = time
            graphics.clear_display_surf(BLUE)        
            for entity in self.entities:            
                dest_rect = pygame.Rect(entity.body.rect.position.x,
                                        entity.body.rect.position.y,
                                        entity.body.rect.w,
                                        entity.body.rect.h)
                graphics.draw(entity.surface, entity.surface_src, dest_rect)
            graphics.flip_display_surf()
            
            self.fps_clock.tick(MAX_FPS)
            
    def at_exit(self):
        """
        Sets the next layer to execute: GameOverLayer or PauseLayer     
        """
        if self.game_status == GameLayer.GAME_PAUSE_SCREEN:
            self.owner.set_layer(self.owner.PAUSE_LAYER)
            self.game_status = GameLayer.GAME_LOOP
        elif self.game_status == GameLayer.GAME_WIN_SCREEN:
            self.owner.set_layer(self.owner.WIN_LAYER)               
        else:
            self.owner.set_layer(self.owner.GAME_OVER_LAYER)
   
    def signal_exit(self):
        self.game_status = GameLayer.GAME_EXIT


class  GameOverLayer:
    """
    Displays the "game over" screen.
    """
    def __init__(self, owner):
        self.owner = owner
        self.text = 'Game Over'
        self.fps_clock = pygame.time.Clock()
        
    def initialize(self, previous_layer):
        self.title_over_surf, self.title_over_rect = graphics.make_text_obj(self.text, TITLE_COLOR,
                                                                           FONT_SIZE_BIG)
        self.title_over_rect.left = (WINDOW_WIDTH - self.title_over_rect.width) / 2
        self.title_over_rect.top = (WINDOW_HEIGHT - self.title_over_rect.height ) / 2    
    
    def run(self):  
        """
        Waits for the user input.
        """           
        while not inputs.is_key_pressed():
            graphics.clear_display_surf(BLACK)
            graphics.get_display_surf().blit(self.title_over_surf, self.title_over_rect)
            graphics.flip_display_surf()
            self.fps_clock.tick(4)
        inputs.clear_event_queue()          
        
    def at_exit(self):
        """
        Sets the next layer to execute: InitLayer.
        """
        self.owner.set_layer(self.owner.INIT_LAYER)


class  PauseLayer:
    """
    Shows the pause screen.
    """
    def __init__(self, owner):
        self.owner = owner
        self.text = 'Pause'
        self.fps_clock = pygame.time.Clock()
        
    def initialize(self, previous_layer):
        self.title_pause_surf, self.title_pause_rect = graphics.make_text_obj(self.text, TITLE_COLOR,
                                                                           FONT_SIZE_BIG)
        self.title_pause_rect.left = (WINDOW_WIDTH - self.title_pause_rect.width) / 2
        self.title_pause_rect.top = (WINDOW_HEIGHT - self.title_pause_rect.height) / 2
    
    def run(self):
        """
        Waits for the user input.
        """
        while not inputs.is_key_pressed():
            graphics.clear_display_surf(BLACK)
            graphics.get_display_surf().blit(self.title_pause_surf, self.title_pause_rect)
            graphics.flip_display_surf()           
            self.fps_clock.tick(4)
        inputs.clear_event_queue()            
        
    def at_exit(self):
        """
        Goes back to GameLayer.
        """
        self.owner.set_layer(self.owner.GAME_LAYER)
        self.game_status = GameLayer.GAME_LOOP
        self.owner.current_layer.run()
        self.owner.current_layer.at_exit()
 
        
class WinLayer:
    """
    Shows the win screen.
    """
    def __init__(self, owner):
        self.owner = owner
        self.text = 'You win!!!'
        self.fps_clock = pygame.time.Clock()
        
    def initialize(self, previous_layer):
        self.title_win_surf, self.title_win_rect = graphics.make_text_obj(self.text, TITLE_COLOR,
                                                                              FONT_SIZE_BIG)
        self.title_win_rect.left = (WINDOW_WIDTH - self.title_win_rect.width) / 2
        self.title_win_rect.top = (WINDOW_HEIGHT - self.title_win_rect.height) / 2
    
    def run(self):
        """
        Waits for the user input.
        """
        while not inputs.is_key_pressed():
            graphics.clear_display_surf(BLACK)
            graphics.get_display_surf().blit(self.title_win_surf, self.title_win_rect)
            graphics.flip_display_surf()           
            self.fps_clock.tick(4)
        inputs.clear_event_queue()            
        
    def at_exit(self):
        """
        Goes back to GameLayer.
        """
        self.owner.set_layer(self.owner.INIT_LAYER)      
