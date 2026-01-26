import pygame
import random
from cell import Cell
from constants import *
from vector import Unit_Vector

def main ():
    pygame.init()

    clock = pygame.time.Clock()
    dt = 0

    pygame.font.init()
    font = pygame.font.SysFont("Candara", 32)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    drawable = pygame.sprite.Group()
    updatable = pygame.sprite.Group()

    Cell.containers = (updatable, drawable)
    Unit_Vector.containers = (updatable, drawable)

    def draw_grid(size):
        grid_total_size = size * SIDE_LENGTH
        
        start_x = (SCREEN_WIDTH // 2) - (grid_total_size // 2)
        start_y = (SCREEN_HEIGHT // 2) - (grid_total_size // 2)

        for i in range(size + 1):
            for j in range(size + 1):
                x = start_x + (i * SIDE_LENGTH)
                y = start_y + (j * SIDE_LENGTH)
                Unit_Vector(x, y, random.randint(0, 359))

                if (i != size and j != size):
                    Cell(x, y, SIDE_LENGTH, random.randint(0, 16), font)


    draw_grid(9)

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
            object.random_switch()        

        pygame.display.flip()

    pygame.quit()

main ()