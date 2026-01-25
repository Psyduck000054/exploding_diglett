# EVERY CELL IS MODELLED HERE

import pygame
from constants import *

class Cell (pygame.sprite.Sprite):
    def __init__ (self, center_x, center_y, side_length):
        self.center_x = center_x
        self.center_y = center_y
        self.side_length = side_length

        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
    
    def draw (self, screen):
        pygame.draw.rect(screen, "white", (self.center_x, self.center_y, self.side_length, self.side_length), 2)

    def update (self):
        pass

