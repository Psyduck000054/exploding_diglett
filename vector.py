import pygame
import math
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