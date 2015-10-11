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


from game_config import WINDOW_WIDTH, WINDOW_HEIGHT 


class Singleton(type):
    _instances = {}
    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(Singleton, self).__call__(*args, **kwargs)
        return self._instances[self]


class Graphics(object):
    """
    Render functions
    """
    __metaclass__ = Singleton
    def __init__(self):
        self.display_surf = pygame.display.set_mode((WINDOW_WIDTH, 
                                                     WINDOW_HEIGHT))
        self.images = {}
    
    def get_display_surf(self):
        return self.display_surf
        
    def clear_display_surf(self, color):
        self.get_display_surf().fill(color)
     
    def flip_display_surf(self):
        pygame.display.flip()   
            
    def make_text_obj(self, text, colour, font_size):
        """
        Render a given text into a surface. Gets the surface its rectangle
        """
        font = pygame.font.Font(None, font_size)
        surf = font.render(text, True, colour)
        return surf, surf.get_rect()
    
    def get_image(self, file_name):
        image = self.images.get(file_name, None)
        if not image:
            image = pygame.image.load(file_name)  
            self.images[file_name] = image 
        return image
    
    def draw(self, surface, src_rect, dest_rect):
        self.get_display_surf().blit(surface.subsurface(src_rect), dest_rect)     
