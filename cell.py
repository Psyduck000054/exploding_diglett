# EVERY CELL IS MODELLED HERE

import pygame
from constants import *
import random

class Cell (pygame.sprite.Sprite):
    #DEFINITION
    def __init__ (self, tl_x, tl_y, side_length, value, font):
        self.tl_x = tl_x
        self.tl_y = tl_y
        self.side_length = side_length
        self.value = value

        #dragon
        self.is_dragon = False
        self.dragon_in_range = False

        #rune
        self.is_rune = False

        #base
        self.is_base = False

        #position in chunk 
        self.cx = 0
        self.cy = 0
        self.rect_color = pygame.Color(0, 0, 0)
        self.font = font

        self.text_surf = self.font.render(str(self.value), True, "black")
        self.text_rect = self.text_surf.get_rect(center=(self.tl_x + self.side_length // 2, 
                                                         self.tl_y + self.side_length // 2))
        
        #inherit from sprite.sprite
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
    
    def draw (self, screen):
        pygame.draw.rect(screen, self.rect_color, (self.tl_x, self.tl_y, self.side_length, self.side_length))
        #pygame.draw.rect(screen, "white", (self.tl_x, self.tl_y, self.side_length, self.side_length), 1)

        screen.blit(self.text_surf, self.text_rect)


    def update_value(self, new_value):
        self.value = new_value
        
        #visual stuff

        #config1: rainbow
        """hue = int(self.value * 280)
        self.rect_color.hsla = (hue, 100, 50, 100)"""

        #config2: map
        
        #special cells
        if self.value == 0: #spawn base
            self.rect_color = "gray"
        elif self.value == 1: #player's spawn point
            self.rect_color = "black"
        elif self.value == 2: #fire dragon
            self.rect_color = "red"
        elif self.value == 3: #dark dragon
            self.rect_color = "purple"
        elif self.value == 4: #rune center
            self.rect_color = "cyan"
        elif self.value == 5: #surroundings
            self.rect_color = "darkslategray"
        
        #terrain cells
        elif self.value < 0.15:
            self.rect_color = "plum"
        elif self.value < 0.25:
            self.rect_color = "mediumslateblue"
        elif self.value < 0.35:
            self.rect_color = "lightblue"
        elif self.value < 0.65:
            self.rect_color = "palegreen"
        elif self.value < 0.75:
            self.rect_color = "lemonchiffon"
        elif self.value < 0.85:
            self.rect_color = "peachpuff"
        elif self.value < 1:
            self.rect_color = "salmon"

            



        

        self.text_surf = self.font.render(str(self.value), True, "black")
        self.text_rect = self.text_surf.get_rect(
            center=(self.tl_x + self.side_length // 2, 
                    self.tl_y + self.side_length // 2)
    )