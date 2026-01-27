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
    dt = 0

    pygame.font.init()
    font = pygame.font.SysFont("Candara", 12)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    drawable = pygame.sprite.Group()

    Cell.containers = (drawable)
    Unit_Vector.containers = (drawable)

    cellList = []
    vectorList = []
    
    def draw_grid(size):
        # init settings here
        grid_total_size = size * SIDE_LENGTH
        start_x = (SCREEN_WIDTH // 2) - (grid_total_size // 2)
        start_y = (SCREEN_HEIGHT // 2) - (grid_total_size // 2)
        cellCol = []
        vectorCol = []
        # add items here
        for i in range(size + 1):
            for j in range(size + 1):
                x = start_x + (i * SIDE_LENGTH)
                y = start_y + (j * SIDE_LENGTH)
                if (i != size and j != size):
                    cellCol.append(Cell(x, y, SIDE_LENGTH, random.randint(-100, 100)/100, font))
                if (i % CHUNK_SIZE == 0 and j % CHUNK_SIZE == 0):
                    vectorCol.append(Unit_Vector(x, y, random.randint(0, 359)))
            cellList.append(cellCol)
            cellCol = []
            if (i % CHUNK_SIZE == 0):
                vectorList.append(vectorCol)
            vectorCol = []

        # test print here
        for i in range (size):
            for j in range (size):
                cellList[i][j].cx = 1/(CHUNK_SIZE * 2) + 1/CHUNK_SIZE * j%CHUNK_SIZE
                cellList[i][j].cy = 1/(CHUNK_SIZE * 2) + 1/CHUNK_SIZE * i%CHUNK_SIZE

        vectorList_len = size//CHUNK_SIZE + (size%CHUNK_SIZE == 0)

        for i in range (vectorList_len):
            for j in range (vectorList_len):
                vectorList[i][j].cx = j
                vectorList[i][j].cy = i
                pass
    draw_grid(SIZE)
    
    # CORNER NOISE STORAGE 3D ARRAY
    #3d array
    noise_cube = []
    #2d subarray
    noise_table = []
    #1d subarray
    noise_line = []
    #the NW, NE, SW, SE
    directions = [[0, 0], [1, 0], [0, 1], [1, 1]]

    for pair in directions:
        for i in range (SIZE):
            for j in range (SIZE):
                x_index = i // CHUNK_SIZE + pair[0]
                y_index = j // CHUNK_SIZE + pair[1]

                #components of vector from cell to corner
                cell_to_corner_x = vectorList[x_index][y_index].cx - cellList[i][j].cx
                cell_to_corner_y = vectorList[x_index][y_index].cy - cellList[i][j].cy

                #dot product
                noise_val = round(dot_product(cell_to_corner_x, cell_to_corner_y, vectorList[x_index][y_index].vx, vectorList[x_index][y_index].vy), 2)
                noise_val *= ENTROPY

                if noise_val > 1:
                    noise_val = 1
                
                if noise_val < -1:
                    noise_val = -1

                noise_line.append(noise_val)

            noise_table.append(noise_line)
            noise_line = []
        noise_cube.append(noise_table)
        noise_table = []

    #MATH [LERP + SMOOTHSTEP]
    for i in range (SIZE):
        for j in range (SIZE):
            #relative position in the chunk
            rel_x = smoothstep(cellList[i][j].cx % 1)
            rel_y = smoothstep(cellList[i][j].cy % 1)

            #NW
            n00 = noise_cube[0][i][j]
            #SW
            n01 = noise_cube[1][i][j]
            #NE
            n10 = noise_cube[2][i][j]
            #SE
            n11 = noise_cube[3][i][j]

            final_noise = round((lerp(lerp(n00, n10, rel_x), lerp(n01, n11, rel_x), rel_y) + 1) / 2, 2)

            cellList[i][j].update_value(final_noise)
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