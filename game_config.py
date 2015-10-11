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


WINDOW_WIDTH = 480
WINDOW_HEIGHT = 800

WHITE = (255, 255, 255) 
BLACK = (0, 0, 0)   
BLUE = (0, 0, 255) 

TITLE_COLOR = WHITE 
  
BRICK_SPACING = 2
BRICK_NUMBER = 7
BRICK_WIDTH = 40 # 40x20 pixels
BRICK_HEIGHT = 20

COUNT_STROKERS = 2 

BRICKS_COLORS = ['pink', 'red', 'blue', 'yellow', 'green', 'grey']

PADDLE_WIDTH = 80 # 80x20 pixels
PADDLE_HEIGHT = 20

BALL_WIDTH = 20 # 20x15 pixels
BALL_HEIGHT = 15

WALL_WIDTH = 500 # 500x500 pixels
WALL_HEIGHT = 500

TEXT_LINE_SPACING = 50  # Vertical space between lines of text.
TEXT_LINE_HORIZONTAL_SPACING = 50  # Horizontal space between lines of text.
FONT_SIZE_BASIC = 25
FONT_SIZE_BIG = 100

STEP_TIME_INTEGRATE = 10 # ms
STEP_TIME = 10 # ms
MAX_FPS = 1000 / STEP_TIME + 1 # Adds +1 in case the division is not exact

PADDLE_VELOCITY = 0.5 # pixels / second

PADDLE_LINE_SPACING = 50 

BALL_VELOCITY_X = 0.242816728473  # pixels / second
BALL_VELOCITY_Y = 0.289631971155 

BALL_PUSH = 6000 # Delay time to automatically push the ball (ms)

IMAGE_FILE_NAME = "textures.png"
