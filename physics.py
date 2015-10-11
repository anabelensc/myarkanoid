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


import vector


class Rect:
    """
    Rectangular body shape
    """
    def __init__(self, position, w, h):
        self.position = position 
        self.w = w 
        self.h = h 
          
    def left(self):
        return self.position.x

    def right(self):
        return self.position.x + self.w

    def top(self):
        return self.position.y

    def bottom(self):
        return self.position.y + self.h

    def center(self):
        return vector.Vector2(self.position.x + self.w * 0.5, self.position.y + self.h * 0.5)


class Body:
    """
    Body for physical objects
    """
    def __init__(self, rect, velocity, object_type, tag_ent, is_static = True):
        self.rect = rect               
        self.set_velocity(vector.magnitude(velocity))
        self.direction = vector.normalize(velocity)
        self.object_type = object_type                   
        self.is_static = is_static
        self.tag_ent = tag_ent
        
    def set_velocity(self, value):
        self.velocity = min(PhysicsWorld.MAX_SPEED, value)

    def integrate(self, elapsed_time):
        if not(self.is_static):
            self.rect.position =  vector.sum(self.rect.position, vector.mul(self.direction, self.velocity * elapsed_time))


class PhysicsWorld:
    MAX_SPEED = 0.6
    def __init__(self, step_ms):
        self.step_ms = step_ms   
        self.remaining_ms = 0.0
        self.bodies = []
        self.list_call_backs = []
    
    def add_body(self, b):
        self.bodies.append(b)
    
    def delete_body(self, b):
        self.bodies.remove(b)  
    
    class CallBack():
        def __init__(self, tb1, tb2, call_back):
            self.tb1 = tb1
            self.tb2 = tb2
            self.call_back = call_back 
    
    def add_callback(self, call_back):
        self.list_call_backs.append(call_back)  
        
    def clear_bodies(self):
        self.bodies = []        
    
    def collide(self, b1, b2):
        """
        Detects the collision between two bodies
        """
        if b1.is_static and b2.is_static:
            return False  
        return not(
            b1.rect.left() >= b2.rect.right() or
            b1.rect.right() <= b2.rect.left() or
            b1.rect.top() >= b2.rect.bottom() or
            b1.rect.bottom() <= b2.rect.top())
    
    def solve_collision(self, b1, b2):
        # Changes the direction of non-static moving bodies, and separates overlapping bodies

        def penetration(normal, movable_body, fixed_body):
            if normal.x < -0.0001:
                return abs(movable_body.rect.right() - fixed_body.rect.left())
            elif normal.x > 0.0001:   
                return abs(fixed_body.rect.right() - movable_body.rect.left())
            if normal.y < -0.0001:                
                return abs(fixed_body.rect.top() - movable_body.rect.bottom())
            else:
                return abs(movable_body.rect.top() - fixed_body.rect.bottom())
            
        if b1.is_static and not(b2.is_static):
            normal = self.calculate_normal(b2, b1)
            pen_distance = penetration(normal, b2, b1)           
            b2.rect.position = vector.sum(b2.rect.position, vector.mul(normal, pen_distance))
            b2.direction = vector.reflect(normal, b2.direction)
            return normal 
        elif not(b1.is_static) and b2.is_static:
            normal = self.calculate_normal(b1, b2)
            pen_distance = penetration(normal, b1, b2)
            b1.rect.position = vector.sum(b1.rect.position, vector.mul(normal, pen_distance))
            b1.direction = vector.reflect(normal, b1.direction)
            return normal  
        elif not(b1.is_static) and not(b2.is_static):
            normal = self.calculate_normal(b1, b2)
            normal_inv = vector.minus(normal)
            pen_distance = penetration(normal, b1, b2)
            b1.rect.set_pos(vector.sum(b1.rect.position, vector.mul(normal, 0.5 * pen_distance)))
            b1.direction = vector.reflect(normal, b1.direction)  
            b2.rect.position = vector.sum(b2.rect.position, vector.mul(normal_inv, 0.5 * pen_distance))               
            b2.direction = vector.reflect(normal_inv, b2.get_direction())
            return normal
        
    def calculate_normal(self, b1, b2):
        """
        Calculates the normal of b1 with respect to b2
        """
        normal_x = 0.0
        normal_y = 0.0    
        
        # Difference between body centers
        center_dir = vector.normalize(vector.sub(b1.rect.center(), b2.rect.center()))

        cos_threshold = b2.rect.w / math.sqrt(math.pow(b2.rect.h, 2) + math.pow(b2.rect.w, 2)) 
        if vector.dot(center_dir, vector.Vector2(1, 0)) >= cos_threshold:
            # b1 is at the right side of b2
            normal_x = 1.0
        elif vector.dot(center_dir, vector.Vector2(-1, 0)) >= cos_threshold:
            # b1 is at the left side of b2
            normal_x = -1.0
        elif vector.dot(center_dir, vector.Vector2(0, -1)) >= math.cos(math.pi * 0.5 - math.acos(cos_threshold)):
            # b1 is above b2
            normal_y = -1.0
        else:
            # b1 is below b2
            normal_y = 1.0
        
        return vector.Vector2(normal_x, normal_y)
       
    def integrate(self):
        # Integrate body velocities
        for b in self.bodies:
            b.integrate(self.step_ms)    
    
    def detect_and_solve_collision(self):       
        # Detect and resolve collisions. Then, call collision callback functions.
        for i in range(len(self.bodies) - 1):
            for j in range(i + 1, len(self.bodies)):                
                if self.collide(self.bodies[i], self.bodies[j]): 
                    normal = self.solve_collision(self.bodies[i], self.bodies[j])   
                    for c in self.list_call_backs:
                        if self.bodies[i].object_type == c.tb1 and self.bodies[j].object_type == c.tb2:
                            c.call_back(self.bodies[i], self.bodies[j], normal)
                        elif self.bodies[j].object_type == c.tb1 and self.bodies[i].object_type == c.tb2:
                            c.call_back(self.bodies[j], self.bodies[i], vector.minus(normal))                
                    
    def step_simulation(self, elapsed_time):
        # Simulate a delta of time
        self.remaining_ms += elapsed_time
        step_count = int(self.remaining_ms / self.step_ms)
        
        for i in range(step_count):
            self.integrate()
            self.detect_and_solve_collision()

        self.remaining_ms -= step_count * self.step_ms
        