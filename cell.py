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
        self.terrain = ""

        #status flags
        self.is_3x3 = False
        self.dragon_in_range = False
        self.is_rune = False
        self.is_base = False

        self.block = []
        add(self.block, [[False, 20]])
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
        if self.is_3x3:
            dragon_w = self.image.get_width() 
            offset = (dragon_w - self.side_length) // 2
            screen.blit(self.image, (self.tl_x - offset, self.tl_y - offset))
        else:
            screen.blit(self.image, (self.tl_x, self.tl_y))
    
    def update_value(self, new_value):
        self.value = new_value
        
        # cell values with multiple textures
        deep_sea = []
        add (deep_sea, [["deep_sea0", 96],
                        ["deep_sea1", 2], 
                        ["deep_sea2", 2]])

        shallow_sea = []
        add (shallow_sea, [["shallow_sea0", 90],
                           ["shallow_sea1", 5],
                           ["shallow_sea2", 5]])

        beach = []
        add (beach, [["beach0", 90],
                     ["beach1", 10],
                     ["beach2", 0]])
        
        grassland = []
        add (grassland, [["grassland0", 90],
                         ["grassland1", 2],
                         ["grassland2", 6],
                         ["grassland3", 2]])
        
        desert = []
        add (desert, [["desert0", 90],
                      ["desert1", 8],
                      ["desert2", 2]])
    
        badlands = []
        add (badlands, [["badlands0", 90],
                        ["badlands1", 5],
                        ["badlands2", 5]])

        # special cells
        if self.value == 0: key = "base"
        elif self.value == 1: key = "spawn"
        elif self.value == 2: key = "rune_chest"
        elif self.value == 3: key = "rune_beacon"
        
        # 3x3 images
        elif self.value == 4:
            key = "fire_dragon"
            if self.is_3x3:
                self.image = Cell.textures["fire_dragon"]
            else:
                self.image = pygame.Surface((self.side_length, self.side_length), pygame.SRCALPHA)
            return
        elif self.value == 5:
            key = "deep_sea_dragon"
            if self.is_3x3:
                self.image = Cell.textures["deep_sea_dragon"]
            else:
                self.image = pygame.Surface((self.side_length, self.side_length), pygame.SRCALPHA)
            return
        elif self.value == 6:
            key = "badlands_3x3"
            if self.is_3x3:
                self.image = Cell.textures["badlands_3x3"]
            else:
                self.image = pygame.Surface((self.side_length, self.side_length), pygame.SRCALPHA)
            return

        elif self.value == 7:
            key = "desert_3x3"
            if self.is_3x3:
                self.image = Cell.textures["desert_3x3"]
            else:
                self.image = pygame.Surface((self.side_length, self.side_length), pygame.SRCALPHA)
            return
        elif self.value == 8:
            key = "grassland_3x3"
            if self.is_3x3:
                self.image = Cell.textures["grassland_3x3"]
            else:
                self.image = pygame.Surface((self.side_length, self.side_length), pygame.SRCALPHA)
            return
        elif self.value == 9:
            key = "beach_3x3"
            if self.is_3x3:
                self.image = Cell.textures["beach_3x3"]
            else:
                self.image = pygame.Surface((self.side_length, self.side_length), pygame.SRCALPHA)
            return


        # terrain
        elif self.value < ABYSS: 
            key = "abyss"
            self.terrain = "abyss"
        elif self.value < DEEP_SEA: 
            key = random.choice(deep_sea)
            self.terrain = "deep_sea"
        elif self.value < SHALLOW_SEA: 
            key = random.choice(shallow_sea)
            self.terrain = "shallow_sea"
        elif self.value < BEACH: 
            key = random.choice(beach)
            self.terrain = "beach"
        elif self.value < GRASSLAND: 
            key = random.choice(grassland)
            self.terrain = "grassland"
        elif self.value < DESERT: 
            self.terrain = "shallow_sea"
            key = random.choice(desert)
        elif self.value < BADLANDS:
            key = random.choice(badlands)
            self.terrain = "badlands"
        else:                    
            key = "lava"
            self.terrain = "badlands"

        # assign the image from the pre-loaded dictionary
        if key in Cell.textures:
            self.image = Cell.textures[key]