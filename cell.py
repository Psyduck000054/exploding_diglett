# EVERY CELL IS MODELLED HERE

import pygame
from constants import *
import random
from add import *

class Cell(pygame.sprite.Sprite):
    #this dictionary will be filled by main.py
    textures = {} 

    def __init__(self, tl_x, tl_y, side_length, value, font):
        self.tl_x = tl_x
        self.tl_y = tl_y
        self.side_length = side_length
        self.value = value

        #status flags
        self.is_dragon = False
        self.dragon_in_range = False
        self.is_rune = False
        self.is_base = False
        self.spawn_proof = False

        self.cx = 0
        self.cy = 0
        self.font = font
        
        # default placeholder surface
        self.image = pygame.Surface((side_length, side_length))
        
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

    def draw(self, screen):
        if self.is_dragon:
            dragon_w = self.image.get_width() 
            offset = (dragon_w - self.side_length) // 2
            screen.blit(self.image, (self.tl_x - offset, self.tl_y - offset))
        else:
            screen.blit(self.image, (self.tl_x, self.tl_y))
    
    def update_value(self, new_value):
        self.value = new_value
        
        # cell values with multiple textures
        deep_sea = []
        add (deep_sea, [["deep_sea0", 80],
                        ["deep_sea1", 10], 
                        ["deep_sea2", 5],
                        ["deep_sea3", 5]])

        shallow_sea = []
        add (shallow_sea, [["shallow_sea0", 80],
                           ["shallow_sea1", 10],
                           ["shallow_sea2", 10]])

        beach = []
        add (beach, [["beach0", 70],
                     ["beach1", 20],
                     ["beach2", 10]])
        
        grassland = []
        add (grassland, [["grassland0", 70],
                         ["grassland1", 10],
                         ["grassland2", 10],
                         ["grassland3", 10],])
        
        desert = []
        add (desert, [["desert0", 60],
                      ["desert1", 10],
                      ["desert2", 25],
                      ["desert3", 5]])
    
        badlands = []
        add (badlands, [["badlands0", 70],
                        ["badlands1", 15],
                        ["badlands2", 15]])

        # special cells
        if self.value == 0: key = "base"
        elif self.value == 1: key = "spawn"
        elif self.value == 2:
            key = "fire_dragon"
            if self.is_dragon:
                self.image = Cell.textures["fire_dragon"]
            else:
                self.image = pygame.Surface((self.side_length, self.side_length), pygame.SRCALPHA)
            return
        elif self.value == 3:
            key = "deep_sea_dragon"
            if self.is_dragon:
                self.image = Cell.textures["deep_sea_dragon"]
            else:
                self.image = pygame.Surface((self.side_length, self.side_length), pygame.SRCALPHA)
            return
        elif self.value == 4: key = "rune_chest"
        elif self.value == 5: key = "rune_beacon"
        
        # terrain
        elif self.value < 0.125: key = "abyss"
        elif self.value < 0.25:  key = random.choice(deep_sea)
        elif self.value < 0.375: key = random.choice(shallow_sea)
        elif self.value < 0.5:   key = random.choice(beach)
        elif self.value < 0.625: key = random.choice(grassland)
        elif self.value < 0.75:  key = random.choice(desert)
        elif self.value < 0.875: key = random.choice(badlands)
        else:                    key = "lava"

        # assign the image from the pre-loaded dictionary
        if key in Cell.textures:
            self.image = Cell.textures[key]