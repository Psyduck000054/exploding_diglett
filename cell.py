# EVERY CELL IS MODELLED HERE

import pygame
from constants import *
import random

class Cell (pygame.sprite.Sprite):
    def __init__ (self, tl_x, tl_y, side_length, value, font):
        self.tl_x = tl_x
        self.tl_y = tl_y
        self.side_length = side_length
        self.value = value

        self.font = font
        self.text_surf = self.font.render(str(self.value), True, "white")
        self.text_rect = self.text_surf.get_rect(center=(self.tl_x + self.side_length // 2, 
                                                         self.tl_y + self.side_length // 2))

        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
    
    def draw (self, screen):
        pygame.draw.rect(screen, "white", (self.tl_x, self.tl_y, self.side_length, self.side_length), 2)
        screen.blit(self.text_surf, self.text_rect)

    def update_value(self, new_value):
        self.value = new_value
        self.text_surf = self.font.render(str(self.value), True, "white")
        self.text_rect = self.text_surf.get_rect(
            center=(self.tl_x + self.side_length // 2, 
                    self.tl_y + self.side_length // 2)
    )
        
    def random_switch (self):
        """ran = random.randint (1, 100)

        if ran <= 1:
            self.update_value(random.randint (1, 16))"""
        return

    def update (self):
        pass

