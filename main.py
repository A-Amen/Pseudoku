import pygame
from grid import grid
import helpers
import const




def main():
    pygame.init()
    screen = pygame.display.set_mode((const.grid_size, const.grid_size))
    pygame.display.set_caption('Pseudoku')
    grid_canvas = pygame.Surface(screen.get_size())
    grid_canvas.fill(const.white_higher)
    helpers.draw_vertical(grid_canvas)
    helpers.draw_horizontal(grid_canvas)
    grid_model = grid("")
    grid_model.init_grid()
    print(grid_model.grid_str)
    clock = pygame.time.Clock()
    helpers.gameloop(clock, screen, grid_canvas, grid_model)
    
    

if __name__ == "__main__":
    main()