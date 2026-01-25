import pygame
from cell import Cell
from constants import *

def main ():
    pygame.init()

    clock = pygame.time.Clock()
    dt = 0

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    drawable = pygame.sprite.Group()
    updatable = pygame.sprite.Group()

    Cell.containers = (updatable, drawable);

    def draw_grid(size):
        grid_total_size = size * SIDE_LENGTH
        
        start_x = (SCREEN_WIDTH // 2) - (grid_total_size // 2)
        start_y = (SCREEN_HEIGHT // 2) - (grid_total_size // 2)

        for i in range(size):
            for j in range(size):
                x = start_x + (i * SIDE_LENGTH)
                y = start_y + (j * SIDE_LENGTH)
                Cell(x, y, SIDE_LENGTH)

    draw_grid(9)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        dt = clock.tick(60)/1000
        print(dt)

        screen.fill("black")
        
        for object in drawable:
            object.draw(screen)
        pygame.display.flip()

    pygame.quit()

main ()