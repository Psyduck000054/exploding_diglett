import pygame
import random
from cell import Cell
from constants import *
from vector import Unit_Vector
from vectormath import *
from beautyprint import *

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
                    vectorCol.append(Unit_Vector(x, y, random.randint(0, 359)))
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
                    angle = math.radians(random.randint(0, 359))
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
    for i in range (SIZE_X//2 - 4, SIZE_X//2 + 6):
        for j in range (SIZE_Y//2 - 4, SIZE_Y//2 + 6):
            cellList[i][j].update_value(0)

    # 

    rangle_deg = 360/NUM_PLAYERS
    rangle_rad = math.radians(rangle_deg)

    # a random start bearing
    start_bearing_deg = random.randint(0, round(rangle_deg))
    bearing_rad = math.radians(start_bearing_deg)

    mid_cell_x = SIZE_X // 2 + 1
    mid_cell_y = SIZE_Y // 2 + 1

    for i in range (NUM_PLAYERS):
        player_init_vector_x = math.floor(4 * math.cos(bearing_rad))
        player_init_vector_y = math.floor(4 * math.sin(bearing_rad))
        print(f"{mid_cell_x + player_init_vector_x}, {mid_cell_y + player_init_vector_y}")
        cellList[mid_cell_x + player_init_vector_x][mid_cell_y + player_init_vector_y].update_value(1)
        bearing_rad += rangle_rad
        

    # RUNNING
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        dt = clock.tick(60)/1000
        # print(dt)

        screen.fill("black")
        
        for object in drawable:
            object.draw(screen)

        pygame.display.flip()

    pygame.quit()

main ()