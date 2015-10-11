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


import game_layers


class Game:
    """
    Controls the game dynamics using five so-called game layers. Each layer provides the
    following interface: 
        + initialize(previous_layer): initializes the layer data. The last running layer
                                      is passed as parameter.
        + run(): iterates until some condition is met.
        + at_exit(): called when run() finishes. This method is intended to transfer the
                    control to any other layer.
    """
    INIT_LAYER = 0
    GAME_LAYER = 1
    GAME_OVER_LAYER = 2
    PAUSE_LAYER = 3
    WIN_LAYER = 4
    
    def __init__(self):
        self.layers = [game_layers.InitLayer(self),
                      game_layers.GameLayer(self), 
                      game_layers.GameOverLayer(self),
                      game_layers.PauseLayer(self),
                      game_layers.WinLayer(self)] 
    
        self.current_layer = None
        self.previous_layer = None
        self.exit_signaled = False
        self.set_layer(self.INIT_LAYER)
        self.exit_signale = False        

    def initialize(self):
        pass

    def run(self):
        """
        Runs the layer functions until termination is signaled through signal_exit()
        """
        while not(self.exit_signaled):
            self.current_layer.initialize(self.previous_layer)
            self.current_layer.run()
            self.current_layer.at_exit()
    
    def set_layer(self, layer_id):
        """
        Changes the layer executed by run()
        """
        self.previous_layer = layer_id
        self.current_layer = self.layers[layer_id]

    def signal_exit(self):
        self.exit_signaled = True
