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


import math

class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return "[ %f, %f ]" % (self.x, self.y)
        
    def vector_init(self, v):
        self.x = v.x
        self.y = v.y

def sum(v1, v2):
    return Vector2(v1.x + v2.x, v1.y + v2.y)

def sub(v1, v2):
    return Vector2(v1.x - v2.x, v1.y - v2.y)

def mul(v, scalar):
    return Vector2(v.x * scalar, v.y * scalar)

def magnitude(v):
    return math.sqrt(v.x * v.x + v.y * v.y)

def dot(v1, v2):
    return v1.x * v2.x + v1.y * v2.y

def normalize(v):
    m = magnitude(v)
    if m > 0.0:
        return Vector2(v.x / m, v.y / m)
    return Vector2(0.0, 0.0)

def minus(v):
    return Vector2(-v.x, -v.y)

def reflect(normal, direction):  
    return normalize(sum(direction, mul(normal, abs(2.0 * dot(direction, normal))))) 

def rotate(v, angle):
    cosA = math.cos(angle)
    sinA = math.sin(angle)
    return Vector2(v.x * cosA - v.y * sinA, v.x * sinA + v.y * cosA)

ZERO2 = Vector2(0.0, 0.0)
