import pygame, const
from grid import grid
pygame.font.init()
font = pygame.font.SysFont('Arial', const.font_size)
def update(screen, canvas):
    screen.blit(canvas, (0, 0))

def draw_vertical(canvas):
    line_sep = const.grid_size / 9
    for vertical in range(1, 10):
        if vertical % 3 == 0:
            # Draw bold line for every 3rd(mini-box outlines)
            pygame.draw.line(canvas, const.black,
                             (vertical * line_sep, 0),
                             (vertical * line_sep, const.grid_size),
                             3)
        else:
            # draw grey line
            pygame.draw.line(canvas, const.grey,
                             (vertical * line_sep, 0),
                             (vertical * line_sep, const.grid_size),
                             1)

def draw_horizontal(canvas):
    line_sep = const.grid_size / 9
    for horizontal in range(1, 10):
        if horizontal % 3 == 0:
            # Draw bold line for every 3rd(mini-box outlines)
            pygame.draw.line(canvas, const.black,
                             (0, horizontal * line_sep),
                             (const.grid_size, horizontal * line_sep),
                             3)
        else:
            # draw grey line
            pygame.draw.line(canvas, const.grey,
                             (0, horizontal * line_sep),
                             (const.grid_size, horizontal * line_sep),
                             1)

def fill_box(canvas, pos, number):
    # Fill a box on canvas at given position with the number

    # Create Surface
    box = pygame.Surface((const.box_size, const.box_size),
                         pygame.SRCALPHA, 32)
    text_surface = font.render(str(number), True, const.black)
    width = text_surface.get_width()
    height = text_surface.get_height()
    offsets = (width // 2, height //2)
    box.blit(text_surface,
             (const.box_size // 2 - offsets[0],
              const.box_size //2 - offsets[1]))
    canvas.blit(box,
                (pos[1] * const.box_size,
                 pos[0] * const.box_size))


def gameloop(clock, screen, canvas, model):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
                # quit()
            elif event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    pygame.quit()
                    break
                    # quit()
        
        update(screen, canvas)
        pygame.display.update()
        clock.tick(30)