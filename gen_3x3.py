from cell import Cell
import random
from constants import *

def gen_3x3 (cell_list, cell_value, min_val, max_val, rate, block_rad=2):
    for i in range (1, SIZE_X - 1):
        for j in range (1, SIZE_Y - 1):
            cell = cell_list[i][j]

            if cell.spawn_proof or cell.block[cell_value]:
                continue

            rng = random.random()

            if ((cell.value > min_val and cell.value < max_val)) and rng < rate:
                cell.spawn_proof = True
                cell.is_3x3 = True

                # draw
                for x in range (i - 1, i + 2):
                    for y in range (j - 1, j + 2):
                        if cell_list[x][y].value % 1 != 0:
                            cell_list[x][y].update_value(cell_value)

                print(f"CELL {cell.value} SPAWNED AT [{i}, {j}]")
                    
                #spawn_proof
                for x in range (max (0, i - 2), min (SIZE_X - 1, i + 3)):
                    for y in range (max (0, j - 2), min (SIZE_Y - 1, j + 3)):
                        cell_list[x][y].spawn_proof = True

                #block same structure from spawning
                for x in range (max (0, i - block_rad), min(SIZE_X, i + block_rad + 1)):
                    for y in range (max (0, j - block_rad), min(SIZE_Y, j + block_rad + 1)):
                        cell_list[x][y].block[cell_value] = True
