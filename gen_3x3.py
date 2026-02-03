from cell import Cell
import random
from constants import *

# count how many of the surrounding 8 cells are its neighbours
def alike_neighbour (cell_list, x, y):
    count = 0
    for i in range (max(0, x - 1), min(SIZE_X - 1, x + 2)):
        for j in range (max(0, y - 1), min(SIZE_Y - 1, y + 2)):
            if x == i and y == j:
                continue
            if cell_list[x][y].terrain == cell_list[i][j].terrain:
                count += 1

    return count


def gen_3x3 (cell_list, cell_value, cell_terrain, rate, block_rad=2, min_neighbours=0):
    for i in range (1, SIZE_X - 1):
        for j in range (1, SIZE_Y - 1):
            cell = cell_list[i][j]

            if cell.spawn_proof or cell.block[cell_value]:
                continue

            rng = random.random()

            if ((cell.terrain == cell_terrain) and rng < rate) and alike_neighbour(cell_list, i, j) >= min_neighbours:
                cell.spawn_proof = True
                cell.is_3x3 = True

                # draw
                for x in range (i - 1, i + 2):
                    for y in range (j - 1, j + 2):
                        if cell_list[x][y].value % 1 != 0:
                            cell_list[x][y].update_value(cell_value)

                print(f"CELL {cell.value} SPAWNED AT [{i}, {j}] WITH {alike_neighbour(cell_list, i, j)} NEIGHBOURS")
                    
                #spawn_proof
                for x in range (max (0, i - 2), min (SIZE_X - 1, i + 3)):
                    for y in range (max (0, j - 2), min (SIZE_Y - 1, j + 3)):
                        cell_list[x][y].spawn_proof = True

                #block same structure from spawning
                for x in range (max (0, i - block_rad), min(SIZE_X, i + block_rad + 1)):
                    for y in range (max (0, j - block_rad), min(SIZE_Y, j + block_rad + 1)):
                        cell_list[x][y].block[cell_value] = True
