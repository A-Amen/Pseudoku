import pygame, const, time
from grid import grid
pygame.font.init()
font = pygame.font.SysFont('Arial', const.font_size)
def update(screen, canvas, number_canvas, finish_canvas, complete):
    """Function that updates the main window with relevant surfaces"""
    # Updates the screen with canvas(background canvas), number_canvas(surface with numbers blitted to it)
    # and finish_canvas(when you finish the pseudoku)
    screen.blit(canvas, (0, 0))
    screen.blit(number_canvas, (0, 0))
    if complete:
        screen.blit(finish_canvas, (0, 0))

def keyboard_handle(keytype, number_canvas, keystring, pos, grid_main, canvas):
    """Function that handles all valid keyboard inputs
        Takes in keytype(not unicode), the canvas to draw to(number_canvas),
        keystring(unicode), position, model and the graphic canvas.
        Either fills the focused block with the keystring or moves focus
        on arrow pad keydown"""
    # Keyboard handle function. 
    replace = False # Whether or not to replace the block at the focus point.
    if keytype in const.valid_keys: # const.keys contains valid keypresses to change an entry
        if keytype == pygame.K_DELETE or keytype == pygame.K_BACKSPACE: 
            keystring = "    " # 4 spaces seems to clear the emoji well off the canvas.
        else:
            if grid_main.get_char_at_focus() != "_":
                replace = True
        focus_pos = (pos % 9, pos // 9) # Relative position in 9x9 grid
        if replace: # If replacing, blit the box at position with blank 
            fill_box(number_canvas, focus_pos, "    ")
        fill_box(number_canvas, focus_pos, keystring) # Blit box with keystring
        # Update model(grid) info
        if keystring == "    ":
            grid_main.fill_at_focus("_")
        else:
            grid_main.fill_at_focus(keystring)
    # Keypresses to shift focus
    elif keytype in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
        # shift focus
        focus_shift = None
        last_focus = grid_main.get_focus()
        if keytype == pygame.K_UP:
            focus_shift = 3
        elif keytype == pygame.K_DOWN:
            focus_shift = 4
        elif keytype == pygame.K_LEFT:
            focus_shift = 1
        else:
            focus_shift = 2
        if grid_main.key_shift_focus(focus_shift):
            focus_block(last_focus, False, canvas)
            focus_block(grid_main.get_focus(), True, canvas)

def grid_pos(mouse_pos):
    """Function that takes in tuple with 2 values(x, y) and outputs the equivalent grid position"""
    # Grid pos returns the grid position as (horizontalPos, verticalPos).
    #  Eg . top left is (0, 0), below it is (0, 1) and the top-right is (8, 0)
    box_horizontal = mouse_pos[0] // const.box_size
    box_vertical = mouse_pos[1] // const.box_size
    return int((box_vertical * 9) + box_horizontal)

def draw_vertical(canvas):
    """Function that draws vertical lines from top to bottom on the graphic canvas(canvas)"""
    # Line separation is always equal to the size of a box
    # Draw one line from top of the canvas to the bottom.
    # Every 3rd line is thicker than the normal lines.
    line_sep = const.box_size
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
    """Function that draws horizontal lines from left to right on the graphic canvas(canvas)"""
    # Same as above, but draws from left to right instead.
    line_sep = const.box_size
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
    """Takes in the number canvas(canvas) and fills the area at position(pos) with the emoji"""
    # Fill a box on canvas at given position with the number
    # Create a square surface of size box_size(see const.py)
    box = pygame.Surface((const.box_size, const.box_size),
                         pygame.SRCALPHA, 32)
    # The file path
    path = "emojis/" + str(number) + ".png"
    emoji_image = None
    if str(number) != "    ":
        emoji_image = pygame.image.load(path)
        emoji_image = pygame.transform.scale(emoji_image, (40, 40))
        emoji_image = emoji_image.convert_alpha()

    # In case we have an empty string, ie "    " , we want the text surface of that.
    text_surface = font.render(str(number), True, const.black)
    width = text_surface.get_width()
    height = text_surface.get_height()
    # This fills the blank surface with plain color(ie an empty box color).
    if str(number) == "    ":
        text_surface.fill(const.plain)
    offsets = (width // 2, height //2)
    # Case to choose which surface to blit, the emoji or the blank text
    if str(number) == "    ":
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

def focus_block(focus_pos, to_focus, canvas):
    """Takes in a position to focus, boolean to focus or unfocus and the graphic canvas(canvas)"""
    # Focus a block at a given position in the canvas.
    # to_focus is a boolean that determines whether to focus or unfocus a block.
    focus_coord = (focus_pos % 9 * const.box_size, focus_pos // 9 * const.box_size)
    # We want the focus box to be ~ 90% of the actual box size. 
    box_dim = (int(const.box_size * 0.9), int(const.box_size * 0.9))
    # It just works.
    x_offset = y_offset = const.box_size * 0.05
    focus_box = pygame.Surface(box_dim)
    if to_focus:
        focus_box.fill(const.focused)
    else:
        focus_box.fill(const.plain)
    canvas.blit(focus_box, (focus_coord[0] + x_offset, focus_coord[1] + y_offset))

def handle_mouse_event(grid_main, canvas):
    """Function that handles all mouse events"""
    # Handles mouse events by determining where the mouse was clicked in the grid
    #  and then applying focus, if applicable.
    mouse_pos = pygame.mouse.get_pos()
    grid_num = grid_pos(mouse_pos)
    # If the position is not focused and is focusable then we proceed to focus it
    if not grid_main.is_focused(grid_num) and grid_main.is_focusable(grid_num):
        # Get the position of the last focus position
        last_focus = grid_main.get_focus() 
        if last_focus != grid_num and last_focus != -1:
            # unfocus the last focused block
            focus_block(last_focus, False, canvas)
        # Focus the block in model.
        grid_main.set_focus_index(grid_num)
        # Focus the block on canvas.
        focus_block(grid_num, True, canvas)

def fill_static_boxes(canvas, grid_main):
    """Function to fill all static boxes from the initial generation of the pseudoku grid."""
    # Small function that fills out initial values from the pseudoku to the canvas.
    # These boxes are static and they cannot be changed in the canvas or the model.
    for i in range(0, len(grid_main.grid_str)):
        box_char = grid_main.grid_str[i]
        if box_char != "_":
            fill_box(canvas, ((i % 9), (i // 9)), box_char)

def quit_game(running):
    """Takes in gameloop's running boolean and sets it to false to quit the loop"""
    # Just quit.
    pygame.quit()
    running = False

def fill_finish_canvas(canvas, start_time, end_time):
    """Takes in the endgame canvas along with start and end timestamps and draws
        the appropriate game completion message"""
    # Solve time in seconds
    solve_time = int(end_time - start_time)
    mins, secs = divmod(solve_time, 60) # Split the seconds into minutes, seconds
    sec_str = "%02d"%secs # String Formatting
    min_str = "%02d"%mins # Same
    time_str = "Success in " +min_str + ":" + sec_str +"!" # Time string
    msg_surf = font.render(time_str, True, (0, 0, 0))
    restart_surf = font.render("Press R to restart. ", True, (0, 0, 0))
    w = canvas.get_width()
    h = canvas.get_height()
    canvas.blit(msg_surf, (w/2 - msg_surf.get_width()/2, h/2 - msg_surf.get_height()))
    canvas.blit(restart_surf, (w/2 - msg_surf.get_width()/2, h/2 + restart_surf.get_height()/2))

def start_game():
    """Function that starts the game"""
    # Screen is the native surface to which we blit other surfaces
    screen = pygame.display.set_mode((const.grid_size, const.grid_size), pygame.SRCALPHA, 32)
    pygame.display.set_caption('Pseudoku')
    icon_surface = pygame.image.load('emojis/icon.png')
    icon_surface = pygame.transform.scale(icon_surface, (32, 32))
    icon_surface.convert()
    pygame.display.set_icon(icon_surface)
    
    # pygame.display.set_icon(icon_surface)
    # Graphic canvas is the surface that displays the background color and dividing borders
    graphic_canvas = pygame.Surface(screen.get_size())
    # Number canvas is the surface that displays the numbers in their boxes in Alpha
    number_canvas = pygame.Surface(screen.get_size(), pygame.SRCALPHA, 32)
    graphic_canvas.fill(const.plain)
    draw_vertical(graphic_canvas)
    draw_horizontal(graphic_canvas)
    # Game over canvas is the canvas that displays the end game message.
    game_over_canvas = pygame.Surface(screen.get_size())
    game_over_canvas.set_alpha(215)
    game_over_canvas.fill(const.white)
    grid_model = grid("")
    grid_model.init_grid()
    grid_model.remove_boxes()
    clock = pygame.time.Clock()
    gameloop(clock, screen, graphic_canvas, number_canvas, grid_model, game_over_canvas)

def gameloop(clock, screen, canvas, number_canvas, grid_main, finish_canvas):
    """Core gameloop of pseudoku. Takes in clock, screen, graphic canvas(canvas), number canvas,
        model(grid_main) and game over canvas(finish_canvas)"""
    running = True # Game loop condition
    complete = False # Is the puzzle complete
    reset = False # To reset or not to reset
    fill_static_boxes(number_canvas, grid_main)
    start_time = time.time()
    end_time = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Quit the game when event has pygame.QUIT in it
                quit_game(running)
            elif event.type == pygame.KEYDOWN: # If keyDOWN
                if complete: 
                    if pygame.key.get_pressed()[pygame.K_r]: # Complete case , R = Reset
                        reset = True
                        running = False
                if pygame.key.get_pressed()[pygame.K_ESCAPE]: # Esc = Quit
                    quit_game(running)
                else:
                    # Handle all keyboard inputs
                    keyboard_handle(event.key, number_canvas, event.unicode, grid_main.get_focus(), grid_main, canvas)
            if event.type == pygame.MOUSEBUTTONUP:
                handle_mouse_event(grid_main, canvas)
        if running:
            # update the screen at 30fps
            update(screen, canvas, number_canvas, finish_canvas, complete)
            pygame.display.update()
            clock.tick(30)
        if  (not complete) and grid_main.is_filled(): 
            # Check if grid is filled upon filling the last cell.
            if  grid_main.is_valid_solution(): # Check if valid
                complete = True # Set complete
                end_time = time.time() # set end time
                fill_finish_canvas(finish_canvas, start_time, end_time) # Set finish canvas
    if reset:
        start_game()
