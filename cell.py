# EVERY CELL IS MODELLED HERE

import pygame
from constants import *
import random
from add import *

TERRAIN_VARIANTS = {
        "deep_sea": [["deep_sea0", 96], 
                     ["deep_sea1", 2], 
                     ["deep_sea2", 2]],
        "shallow_sea": [["shallow_sea0", 90], 
                        ["shallow_sea1", 5],
                        ["shallow_sea2", 5]],
        "beach": [["beach0", 90],
                  ["beach1", 5], 
                  ["beach2", 5]],
        "grassland": [["grassland0", 90], 
                      ["grassland1", 2], 
                      ["grassland2", 6], 
                      ["grassland3", 2]],
        "desert": [["desert0", 90], 
                   ["desert1", 8], 
                   ["desert2", 2]],
        "badlands": [["badlands0", 90], 
                     ["badlands1", 5], 
                     ["badlands2", 5]],
        "abyss": [["abyss0", 90], 
                  ["abyss1", 5], 
                  ["abyss2", 5]]
}


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
            cell_w = self.image.get_width() 
            offset = (cell_w - self.side_length) // 2
            screen.blit(self.image, (self.tl_x - offset, self.tl_y - offset))
        else:
            screen.blit(self.image, (self.tl_x, self.tl_y))
    
    def update_value(self, new_value):
        self.value = new_value
        key = None

        # int noise values
        if isinstance(self.value, int) or self.value == 0:
            special_keys = {
                0: "base",
                1: "spawn", 
                2: "rune_chest", 
                3: "rune_beacon",
                4: "fire_dragon", 
                5: "deep_sea_dragon",
                6: "badlands_3x3",
                7: "desert_3x3", 
                8: "grassland_3x3", 
                9: "beach_3x3", 
                10: "shallow_sea_3x3", 
                11: "deep_sea_3x3"
            }
            key = special_keys.get(self.value)
            
            # 3x3 logic
            if 4 <= self.value <= 11:
                if not self.is_3x3:
                    self.image = pygame.Surface((self.side_length, self.side_length), pygame.SRCALPHA)
                    return
        
        # float noise values
        else:
            if self.value < ABYSS: 
                self.terrain = "abyss"
            elif self.value < DEEP_SEA: 
                self.terrain = "deep_sea"
            elif self.value < SHALLOW_SEA: 
                self.terrain = "shallow_sea"
            elif self.value < BEACH: 
                self.terrain = "beach"
            elif self.value < GRASSLAND: 
                self.terrain = "grassland"
            elif self.value < DESERT: 
                self.terrain = "desert"
            elif self.value < BADLANDS:
                self.terrain = "badlands"
            else:
                self.terrain, key = "lava", "lava"

            if key is None:
                variants = []
                add(variants, TERRAIN_VARIANTS[self.terrain])
                key = random.choice(variants)

        if key in Cell.textures:
            original_img = Cell.textures[key]
                        
            fixed_orientation = ["base", "spawn", "rune_chest", "rune_beacon", "fire_dragon", "deep_sea_dragon",
                                 "abyss", "abyss0", "abyss1", "abyss2"]
            
            if key in fixed_orientation:
                self.image = original_img
            else:
                rotation_angle = random.choice([0, 90, 180, 270])
                self.image = pygame.transform.rotate(original_img, rotation_angle)



        