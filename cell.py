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
        add (deep_sea, [["deep_sea0", 90],
                        ["deep_sea1", 5], 
                        ["deep_sea2", 5]])

        shallow_sea = []
        add (shallow_sea, [["shallow_sea0", 80],
                           ["shallow_sea1", 10],
                           ["shallow_sea2", 10]])

        beach = []
        add (beach, [["beach0", 90],
                     ["beach1", 10],
                     ["beach2", 0]])
        
        grassland = []
        add (grassland, [["grassland0", 80],
                         ["grassland1", 5],
                         ["grassland2", 10],
                         ["grassland3", 5]])
        
        desert = []
        add (desert, [["desert0", 88],
                      ["desert1", 10],
                      ["desert2", 2]])
    
        badlands = []
        add (badlands, [["badlands0", 80],
                        ["badlands1", 10],
                        ["badlands2", 10]])

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
        elif self.value == 6:
            key = "desert3"
            if self.is_dragon:
                self.image = Cell.textures["desert3"]
            else:
                self.image = pygame.Surface((self.side_length, self.side_length), pygame.SRCALPHA)
            return
        
        # terrain
        elif self.value < ABYSS: key = "abyss"
        elif self.value < DEEP_SEA: key = random.choice(deep_sea)
        elif self.value < SHALLOW_SEA: key = random.choice(shallow_sea)
        elif self.value < BEACH: key = random.choice(beach)
        elif self.value < GRASSLAND: key = random.choice(grassland)
        elif self.value < DESERT: key = random.choice(desert)
        elif self.value < BADLANDS: key = random.choice(badlands)
        else:                    key = "lava"

        # assign the image from the pre-loaded dictionary
        if key in Cell.textures:
            self.image = Cell.textures[key]