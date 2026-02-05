import pygame
from constants import *
import random
from add import *
from hash_rng import *

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
    textures = {} 

    def __init__(self, tl_x, tl_y, side_length, value, font):
        self.tl_x = tl_x
        self.tl_y = tl_y
        self.side_length = side_length
        self.value = value
        self.terrain = ""
        self.is_3x3 = False
        self.block = [False] * 21
        self.spawn_proof = False
        self.cx = 0
        self.cy = 0
        self.font = font
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
    
    def update_value(self, new_value, rng_system=None, force_terrain=None):
        self.value = new_value
        key = None

        if force_terrain:
            self.terrain = force_terrain

        # rng
        def get_choice(items):
            if rng_system:
                return rng_system.choice(items)
            return random.choice(items)

        def get_int_choice(options): 
            if rng_system:
                return rng_system.choice(options)
            return random.choice(options)

        # shark
        if self.value == 10 and self.is_3x3:
            variants = []
            add(variants, TERRAIN_VARIANTS.get(self.terrain, [["deep_sea0", 100]]))
            bg_key = get_choice(variants) 
            
            if bg_key in Cell.textures and "shark" in Cell.textures:
                bg_img = Cell.textures[bg_key]
                bg_img = pygame.transform.rotate(bg_img, get_int_choice([0, 90, 180, 270]))
                
                shark_img = Cell.textures["shark"]
                shark_rotation = get_int_choice([0, 90, 180, 270])
                
                # --- FIXED LINE BELOW ---
                shark_img = pygame.transform.rotate(shark_img, shark_rotation) 
                # ------------------------
                
                composite = pygame.Surface(shark_img.get_size(), pygame.SRCALPHA)
                composite.blit(bg_img, (self.side_length, self.side_length))
                composite.blit(shark_img, (0, 0))
                
                self.image = composite
                return 
        
        # special tiles
        if isinstance(self.value, int) or self.value == 0:
            special_keys = {
                0: "base", 1: "spawn", 2: "rune_chest", 3: "rune_beacon",
                4: "fire_dragon", 5: "deep_sea_dragon", 6: "badlands_3x3",
                7: "desert_3x3", 8: "grassland_3x3", 9: "beach_3x3", 10: "shark"
            }
            key = special_keys.get(self.value)
            
            if 4 <= self.value <= 9: 
                if not self.is_3x3:
                    self.image = pygame.Surface((self.side_length, self.side_length), pygame.SRCALPHA)
                    return
        else:
            if self.value < ABYSS: self.terrain = "abyss"
            elif self.value < DEEP_SEA: self.terrain = "deep_sea"
            elif self.value < SHALLOW_SEA: self.terrain = "shallow_sea"
            elif self.value < BEACH: self.terrain = "beach"
            elif self.value < GRASSLAND: self.terrain = "grassland"
            elif self.value < DESERT: self.terrain = "desert"
            elif self.value < BADLANDS: self.terrain = "badlands"
            else: self.terrain, key = "lava", "lava"

        if (key is None) or (self.value == 10 and not self.is_3x3):
            variants = []
            add(variants, TERRAIN_VARIANTS.get(self.terrain, [["deep_sea0", 100]]))
            key = get_choice(variants)

        if key in Cell.textures:
            original_img = Cell.textures[key]
            fixed_orientation = ["base", "spawn", "rune_chest", "rune_beacon", "fire_dragon", "deep_sea_dragon",
                                 "abyss", "abyss0", "abyss1", "abyss2"]
            
            if key in fixed_orientation:
                self.image = original_img
            else:
                self.image = pygame.transform.rotate(original_img, get_int_choice([0, 90, 180, 270]))