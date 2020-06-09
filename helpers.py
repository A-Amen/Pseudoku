import pygame, const
from grid import grid
pygame.font.init()
font = pygame.font.SysFont('Arial', const.font_size)
def update(screen, canvas, number_canvas):
    screen.blit(canvas, (0, 0))
    screen.blit(number_canvas, (0, 0))

def keyboard_handle(keytype, canvas, keystring, pos, replace):
    if keytype in const.valid_keys:
        if keytype == pygame.K_DELETE or keytype == pygame.K_BACKSPACE:
            keystring = "  "
        focus_pos = (pos % 9, pos // 9)
        if replace:
            fill_box(canvas, focus_pos, "  ")
        fill_box(canvas, focus_pos, keystring)

def grid_pos(mouse_pos):
    box_horizontal = mouse_pos[0] // const.box_size
    box_vertical = mouse_pos[1] // const.box_size
    return int((box_vertical * 9) + box_horizontal)
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

    if number == "  ":
        text_surface.fill(const.plain)
        # text_surface.fill(const.plain)

    offsets = (width // 2, height //2)
    box.blit(text_surface,
             (const.box_size // 2 - offsets[0],
              const.box_size //2 - offsets[1]))
    canvas.blit(box,
                (pos[0] * const.box_size,
                 pos[1] * const.box_size))

def focus_block(last_focus, to_focus, canvas):
    focus_coord = (last_focus % 9 * const.box_size, last_focus // 9 * const.box_size)
    box_dim = (int(const.box_size * 0.9), int(const.box_size * 0.9))
    x_offset = y_offset = const.box_size * 0.05
    focus_box = pygame.Surface(box_dim)
    if to_focus:
        focus_box.fill(const.focused)
    else:
        focus_box.fill(const.plain)
    canvas.blit(focus_box, (focus_coord[0] + x_offset, focus_coord[1] + y_offset))

def handle_mouse_event(grid_main, canvas):
    mouse_pos = pygame.mouse.get_pos()
    grid_num = grid_pos(mouse_pos)
    # print(grid_num)
    if not grid_main.is_focused(grid_num) and grid_main.is_focusable(grid_num):
        last_focus = grid_main.get_focus()
        if last_focus != grid_num and last_focus != -1:
            # unfocus the last focused block
            focus_block(last_focus, False, canvas)
                    # Set new focus block
        grid_main.set_focus_index(grid_num)
                    # Focus
        focus_block(grid_num, True, canvas)

def quit_game(running):
    pygame.quit()
    running = False
def gameloop(clock, screen, canvas, number_canvas, grid_main):
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(running)
            elif event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    quit_game(running)
                else:
                    # Have a separate Surface/Canvas for numbers
                    if  not event.key == pygame.K_BACKSPACE or  not event.key == pygame.K_DELETE and not grid_main.is_blank(grid_main.get_focus()):
                        replace = False
                        if grid_main.get_char_at_focus() != '_':
                            replace = True
                        keyboard_handle(event.key, number_canvas, event.unicode, grid_main.get_focus(), replace)
                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        grid_main.fill_at_focus("_")
                    else:
                        grid_main.fill_at_focus(event.unicode)
                    # quit()
            if event.type == pygame.MOUSEBUTTONUP:
                handle_mouse_event(grid_main, canvas)
        if running:
            update(screen, canvas, number_canvas)
            pygame.display.update()
            clock.tick(30)
