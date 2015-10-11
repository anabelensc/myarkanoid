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


import utils


def check_for_quit(): 
    """
    Checks if the user has pressed the EXIT button
    """     
    for event in pygame.event.get(pygame.QUIT):
        utils.terminate()
    for event in pygame.event.get(pygame.KEYUP):
        if event.key == pygame.K_ESCAPE:
            utils.terminate() 
        pygame.event.post(event)
   
def is_key_pressed():
    """
    Checks if the user has pressed a button
    """  
    check_for_quit()
    for event in pygame.event.get([pygame.KEYDOWN]):
        if event.type == pygame.KEYDOWN:
            return event.key
    return None

def clear_event_queue():
        """
        Clears the event queue
        """  
        pygame.event.clear()
                