import pygame, const, time
from grid import grid
pygame.font.init()
font = pygame.font.SysFont('Arial', const.font_size)
def update(screen, canvas, number_canvas, finish_canvas, complete):
    screen.blit(canvas, (0, 0))
    screen.blit(number_canvas, (0, 0))
    if complete:
        screen.blit(finish_canvas, (0, 0))

def keyboard_handle(keytype, canvas, keystring, pos, grid_main):
    replace = False
    if keytype in const.valid_keys:
        if keytype == pygame.K_DELETE or keytype == pygame.K_BACKSPACE:
            keystring = "    "
        else:
            if grid_main.get_char_at_focus() != "_":
                replace = True
        focus_pos = (pos % 9, pos // 9)
        if replace:
            fill_box(canvas, focus_pos, "    ")
        fill_box(canvas, focus_pos, keystring)
        if keystring == "    ":
            grid_main.fill_at_focus("_")
        else:
            grid_main.fill_at_focus(keystring)

def grid_pos(mouse_pos):
    # Grid pos returns the grid position as (horizontalPos, verticalPos).
    #  Eg . top left is (0, 0), below it is (0, 1) and the top-right is (8, 0)
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
    path = "emojis/" + str(number) + ".png"
    emoji_image = None
    if str(number) != "    ":
        emoji_image = pygame.image.load(path)
        emoji_image = pygame.transform.scale(emoji_image, (40, 40))
        emoji_image = emoji_image.convert_alpha()
    text_surface = font.render(str(number), True, const.black)
    width = text_surface.get_width()
    height = text_surface.get_height()
    if number == "    ":
        text_surface.fill(const.plain)
    offsets = (width // 2, height //2)
    if number == "    ":
        box.blit(text_surface,
                (const.box_size // 2 - offsets[0],
                const.box_size //2 - offsets[1]))
    else:
        box.blit(emoji_image,
                (const.box_size // 2 - 20 ,
                const.box_size //2 - 20))
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
    # Handles mouse events.
    mouse_pos = pygame.mouse.get_pos()
    grid_num = grid_pos(mouse_pos) 
    if not grid_main.is_focused(grid_num) and grid_main.is_focusable(grid_num):
        last_focus = grid_main.get_focus()
        if last_focus != grid_num and last_focus != -1:
            # unfocus the last focused block
            focus_block(last_focus, False, canvas)
                    # Set new focus block
        grid_main.set_focus_index(grid_num)
                    # Focus
        focus_block(grid_num, True, canvas)

def fill_static_boxes(canvas, grid_main):
    for i in range(0, len(grid_main.grid_str)):
        box_char = grid_main.grid_str[i]
        if box_char != "_":
            fill_box(canvas, ((i % 9), (i // 9)), box_char)

def quit_game(running):
    pygame.quit()
    running = False

def fill_finish_canvas(canvas, start_time, end_time):
    solve_time = int(end_time - start_time)
    mins, secs = divmod(solve_time, 60)
    sec_str = "%02d"%secs
    min_str = "%02d"%mins
    time_str = "Success in " +min_str + ":" + sec_str +"!"
    text_surf = font.render(time_str, True, (0, 0, 0))
    restart_surf = font.render("Press R to restart. ", True, (0, 0, 0))
    w = canvas.get_width()
    h = canvas.get_height()
    # print(end_time - start_time)
    canvas.blit(text_surf, (w/2 - text_surf.get_width()/2, h/2 - text_surf.get_height()))
    canvas.blit(restart_surf, (w/2 - text_surf.get_width()/2, h/2 + restart_surf.get_height()/2))
    # canvas.blit(restart_surf, (w/2 ))

def start_game():
    screen = pygame.display.set_mode((const.grid_size, const.grid_size), pygame.SRCALPHA, 32)
    pygame.display.set_caption('Pseudoku')
    graphic_canvas = pygame.Surface(screen.get_size())
    number_canvas = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
    graphic_canvas.fill(const.plain)
    draw_vertical(graphic_canvas)
    draw_horizontal(graphic_canvas)
    game_over_canvas = pygame.Surface(screen.get_size())
    game_over_canvas.set_alpha(215)
    game_over_canvas.fill(const.white)
    grid_model = grid("")
    grid_model.init_grid()
    grid_model.remove_boxes()
    clock = pygame.time.Clock()
    gameloop(clock, screen, graphic_canvas, number_canvas, grid_model, game_over_canvas)

def gameloop(clock, screen, canvas, number_canvas, grid_main, finish_canvas):
    running = True
    complete = False
    reset = False
    fill_static_boxes(number_canvas, grid_main)
    start_time = time.time()
    end_time = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game(running)
            elif event.type == pygame.KEYDOWN:
                if complete:
                    if pygame.key.get_pressed()[pygame.K_r]:
                        reset = True
                        running = False
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    quit_game(running)
                else:
                    keyboard_handle(event.key, number_canvas, event.unicode, grid_main.get_focus(), grid_main)
            if event.type == pygame.MOUSEBUTTONUP:
                handle_mouse_event(grid_main, canvas)
        if running:
            update(screen, canvas, number_canvas, finish_canvas, complete)
            pygame.display.update()
            clock.tick(30)
        if  (not complete) and grid_main.is_filled():
            if  grid_main.is_valid_solution():
                complete = True
                end_time = time.time()
                fill_finish_canvas(finish_canvas, start_time, end_time)

    if reset:
        start_game()