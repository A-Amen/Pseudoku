import pygame
from grid import grid
import helpers
import const

def main():
    pygame.init()
    screen = pygame.display.set_mode((const.grid_size, const.grid_size), pygame.SRCALPHA, 32)
    pygame.display.set_caption('Pseudoku')
    graphic_canvas = pygame.Surface(screen.get_size())
    number_canvas = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
    graphic_canvas.fill(const.plain)
    helpers.draw_vertical(graphic_canvas)
    helpers.draw_horizontal(graphic_canvas)
    grid_model = grid("")
    grid_model.init_grid()
    print(grid_model.grid_str)
    clock = pygame.time.Clock()
    helpers.gameloop(clock, screen, graphic_canvas, number_canvas, grid_model)

if __name__ == "__main__":
    main()
