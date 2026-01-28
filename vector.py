import pygame
import math
import random
from constants import *

class Unit_Vector(pygame.sprite.Sprite):
    # bearing 0 = N, bearing 90 = E
    def __init__ (self, x_base, y_base, bearing):
        self.x_base = x_base
        self.y_base = y_base
        self.bearing = bearing

        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        
        #radian form to use 
        self.rad = math.radians(self.bearing)

        #vector components
        self.vx = math.sin(self.rad)
        self.vy = math.cos(self.rad)

        #position in chunk
        self.cx = 0
        self.cy = 0

    def draw(self, screen):
        """rad = math.radians(self.bearing)

        x_head = self.x_base + VECTOR_LENGTH * math.sin(rad)
        y_head = self.y_base - VECTOR_LENGTH * math.cos(rad)

        pygame.draw.line(screen, "magenta", (self.x_base, self.y_base), (x_head, y_head), 2)
        pygame.draw.circle(screen, "magenta", (int(x_head), int(y_head)), 2)"""
        pass