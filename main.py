import pygame
import random
from cell import Cell
from constants import *
from vector import Unit_Vector
from vectormath import *
from gen_3x3 import *
from hash import *
from hash_rng import temu_rng

# seed initialization
seed = random.randint(INT64_MIN, INT64_MAX)
print (seed)

rng = temu_rng(seed)

def main ():
    pygame.init()

    clock = pygame.time.Clock()

    pygame.font.init()
    font = pygame.font.SysFont("Candara", 6)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    drawable = pygame.sprite.Group()

    Cell.containers = (drawable)
    Unit_Vector.containers = (drawable)

    cellList = []
    vectorList = []

    def load_all_textures():
        tex = {}

        files = {
            "base": "spawn_base.png",
            "spawn": "spawn_point.png",
            "rune_chest": "rune_chest.png",
            "rune_beacon": "rune_beacon.png",
            
            "abyss0": "abyss0.png", 
            "abyss1": "abyss1.png", 
            "abyss2": "abyss2.png", 

            "deep_sea0": "deep_sea0.png",
            "deep_sea1": "deep_sea1.png",
            "deep_sea2": "deep_sea2.png",

            "shallow_sea0": "shallow_sea0.png",
            "shallow_sea1": "shallow_sea1.png",
            "shallow_sea2": "shallow_sea2.png",

            "beach0": "beach0.png",
            "beach1": "beach1.png",
            "beach2": "beach2.png",
            "beach_3x3": "beach_3x3.png",

            "grassland0": "grassland0.png",
            "grassland1": "grassland1.png",
            "grassland2": "grassland2.png",
            "grassland3": "grassland3.png",
            "grassland_3x3": "grassland_3x3.png",

            "desert0": "desert0.png",
            "desert1": "desert1.png",
            "desert2": "desert2.png",
            "desert_3x3": "desert_3x3.png",

            "badlands0": "badlands0.png",
            "badlands1": "badlands1.png",
            "badlands2": "badlands2.png",
            "badlands_3x3": "badlands_3x3.png",
            
            "lava": "lava.png",

            "fire_dragon": "fire_dragon.png",
            "deep_sea_dragon": "deep_sea_dragon.png",
            "shark": "shark_invis.png"
        }
        
        for key, filename in files.items():
            try:
                img = pygame.image.load(f"assets/{filename}").convert_alpha()

                enlarged_list = ["fire_dragon", "deep_sea_dragon", "desert_3x3", "badlands_3x3", "grassland_3x3", "beach_3x3", 
                                 "shallow_sea_3x3", "deep_sea_3x3", "shark"]
                # scale items in enlarged_list to 3x3 cells, everything else to 1x1
                if key in enlarged_list:
                    tex[key] = pygame.transform.scale(img, (SIDE_LENGTH * 3, SIDE_LENGTH * 3))
                else:
                    tex[key] = pygame.transform.scale(img, (SIDE_LENGTH, SIDE_LENGTH))
                
            except:
                if key in enlarged_list:
                    size = SIDE_LENGTH * 3
                else:
                    size = SIDE_LENGTH

                fallback = pygame.Surface((size, size))
                fallback.fill("magenta") 
                tex[key] = fallback
        
        return tex

        # initialize the textures
    Cell.textures = load_all_textures()

    #DRAW GRID
    def draw_grid(size_x, size_y):
        # init settings here
        grid_total_size_x = size_x * SIDE_LENGTH
        grid_total_size_y = size_y * SIDE_LENGTH

        start_x = (SCREEN_WIDTH // 2) - (grid_total_size_x // 2)
        start_y = (SCREEN_HEIGHT // 2) - (grid_total_size_y // 2)
        cellCol = []
        vectorCol = []
        # add items here
        for i in range(size_x + 1):
            for j in range(size_y + 1):
                x = start_x + (i * SIDE_LENGTH)
                y = start_y + (j * SIDE_LENGTH)
                if (i != size_x and j != size_y):
                    cellCol.append(Cell(x, y, SIDE_LENGTH, 0, font))
                if (i % MIN_CHUNK_SIZE == 0 and j % MIN_CHUNK_SIZE == 0):
                    angle = rng.randint(0, 359)
                    vectorCol.append(Unit_Vector(x, y, angle))
            if i < size_x:
                cellList.append(cellCol)
            cellCol = []
            if (i % MIN_CHUNK_SIZE == 0):
                vectorList.append(vectorCol)
            vectorCol = []

        # test print here
        for i in range (size_x):
            for j in range (size_y):
                cellList[i][j].cx = i
                cellList[i][j].cy = j

        vectorList_len_x = len(vectorList)
        vectorList_len_y = len(vectorList[0])

        for i in range (vectorList_len_x):
            for j in range (vectorList_len_y):
                vectorList[i][j].cx = i
                vectorList[i][j].cy = j
                pass
    draw_grid(SIZE_X, SIZE_Y)

    #OCTAVE NOISE GENERATOR | USE_PREDEFINED ON FOR THE FIRST TIME ONLY | RETURNS A TABLE
    def get_octave_noise(chunk_size, use_predefined=False):
        v_cols = (SIZE_X // chunk_size) + 1
        v_rows = (SIZE_Y // chunk_size) + 1
        gradients = []
        
        if use_predefined:
            for i in range(v_cols):
                row = []
                for j in range(v_rows):
                    row.append((vectorList[i][j].vx, vectorList[i][j].vy))
                gradients.append(row)
        else:
            for i in range(v_cols):
                row = []
                for j in range(v_rows):
                    angle = math.radians(rng.randint(0, 359))
                    row.append((math.sin(angle), math.cos(angle)))
                gradients.append(row)

        # MATH [LERP + SMOOTHSTEP]
        noise_map = [[0 for _ in range(SIZE_Y)] for _ in range(SIZE_X)]
        for i in range(SIZE_X):
            for j in range(SIZE_Y):

                x = i / chunk_size
                y = j / chunk_size
                
                x0 = int(x)
                x1 = x0 + 1
                y0 = int(y)
                y1 = y0 + 1

                sx = smoothstep(x - x0)
                sy = smoothstep(y - y0)

                n0 = entropy_calc(dot_product(x - x0, y - y0, gradients[x0][y0][0], gradients[x0][y0][1]), ENTROPY)
                n1 = entropy_calc(dot_product(x - x1, y - y0, gradients[x1][y0][0], gradients[x1][y0][1]), ENTROPY)
                ix0 = lerp(n0, n1, sx)

                n0 = entropy_calc(dot_product(x - x0, y - y1, gradients[x0][y1][0], gradients[x0][y1][1]), ENTROPY)
                n1 = entropy_calc(dot_product(x - x1, y - y1, gradients[x1][y1][0], gradients[x1][y1][1]), ENTROPY)
                ix1 = lerp(n0, n1, sx)

                noise_map[i][j] = lerp(ix0, ix1, sy)
        return noise_map
    
    #FRACTAL NOISE CALCULATOR
    order = round(math.log(CHUNK_SIZE / MIN_CHUNK_SIZE, SCALE)) + 1
    
    # storage for generated octaves
    generated_octaves = []
    for k in range(order):
        current_chunk_size = MIN_CHUNK_SIZE * pow(SCALE, k)
        is_secondary = (k > 0)
        octave_map = get_octave_noise(current_chunk_size, is_secondary)
        generated_octaves.append(octave_map)

    #calc loop
    for i in range(SIZE_X):
        for j in range(SIZE_Y):
            final_noise = 0
            total_weight = 0
            
            for k in range(order):
                val = (generated_octaves[k][i][j] + 1) / 2
                
                weight = pow(ROUGHNESS, k)
                final_noise += val * weight
                total_weight += weight
            
            final_noise = round(final_noise / total_weight, 2)
            cellList[i][j].update_value(final_noise)

    # SPAWN POINT GENERATION
    # assume the map are even x even, the middle 8x8 block will be used as a spawn point.

    # spawn base initiation
    for i in range (SIZE_X//2 - 7, SIZE_X//2 + 7):
        for j in range (SIZE_Y//2 - 7, SIZE_Y//2 + 7):
            cellList[i][j].spawn_proof = True
            cellList[i][j].block[0] = True

            if (((i >= SIZE_X//2 - 5) and (i <= SIZE_X//2 + 4)) and (j >= SIZE_Y//2 - 5) and (j <= SIZE_Y//2 + 4)):
                cellList[i][j].update_value(0)

    rangle_deg = 360/NUM_PLAYERS
    rangle_rad = math.radians(rangle_deg)

    # a random start bearing
    start_bearing_deg = rng.randint(0, round(rangle_deg))
    bearing_rad = math.radians(start_bearing_deg)

    mid_cell_x = SIZE_X // 2
    mid_cell_y = SIZE_Y // 2

    for i in range (NUM_PLAYERS):
        player_init_vector_x = math.floor(4 * math.cos(bearing_rad))
        player_init_vector_y = math.floor(4 * math.sin(bearing_rad))
        cellList[mid_cell_x + player_init_vector_x][mid_cell_y + player_init_vector_y].update_value(1)
        bearing_rad += rangle_rad
    
    # RUNE SPAWN
    for i in range (1, SIZE_X - 1):
        for j in range (1, SIZE_Y - 1):
            if cellList[i][j].spawn_proof == 1: #no dragon or base
                continue
            luck = rng.random()
            cell = cellList[i][j]

            if (cell.value > SHALLOW_SEA and cell.value < DESERT) and luck < RUNE_SPAWN_RATE:
                cell.spawn_proof = True
                cell.update_value(2)
                print(f"CELL 2 SPAWNED AT [{i}, {j}]")

                
                adjacent_cell = [[1, 0], [0, 1], [-1, 0], [0, -1]] #four adjacent cells
                for pair in adjacent_cell:
                    if cellList[min(max(0, i + pair[0]), SIZE_X - 1)][min(max(0, j + pair[1]), SIZE_Y - 1)].value % 1 != 0:
                        cellList[min(max(0, i + pair[0]), SIZE_X - 1)][min(max(0, j + pair[1]), SIZE_Y - 1)].is_rune = True
                        cellList[min(max(0, i + pair[0]), SIZE_X - 1)][min(max(0, j + pair[1]), SIZE_Y - 1)].update_value(3)
                
                for x in range (max (0, i - 2), min (SIZE_X - 1, i + 3)):
                    for y in range (max (0, j - 2), min (SIZE_Y - 1, j + 3)):
                        cellList[x][y].spawn_proof = True
    
    
    gen_3x3(cellList, 4, ["lava"], DRAGON_SPAWN_RATE, rng, DRAGON_SEPARATION)
    gen_3x3(cellList, 5, ["abyss"], DRAGON_SPAWN_RATE, rng, DRAGON_SEPARATION)
    gen_3x3(cellList, 6, ["badlands"], MINESHAFT_SPAWN_RATE, rng, MINESHAFT_SEPARATION, 4)
    gen_3x3(cellList, 7, ["desert"], OASIS_SPAWN_RATE, rng, OASIS_SEPARATION, 6)
    gen_3x3(cellList, 8, ["grassland"], FRUIT_TREE_SPAWN_RATE, rng, FRUIT_TREE_SEPARATION, 8)
    gen_3x3(cellList, 9, ["beach"], COCONUT_CANOPY_SPAWN_RATE, rng, COCONUT_CANOPY_SEPARATION, 6)
    gen_3x3(cellList, 10, ["shallow_sea", "deep_sea", "abyss"], SHARK_SPAWN_RATE, rng, SHARK_SEPARATION, 8, True)
    
    # RUNNING
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        dt = clock.tick(60)/1000
        # print(dt)

        screen.fill("black")
        
        # draw all standard tiles first
        for object in drawable:
            if hasattr(object, "is_3x3") and not object.is_3x3:
                object.draw(screen)
        
        # then draw 3x3 objects on top
        for object in drawable:
            if getattr(object, "is_3x3", False):
                object.draw(screen)

        pygame.display.flip()

    pygame.quit()

main ()