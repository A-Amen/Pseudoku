import const, random
class grid:
    """Model that holds the grid as a string, along with grid specific variables like
        focus position and all indice that are focusable"""
    def __init__(self, grid_str, focus = -1, focus_indice = -1):
        self.grid_str = grid_str
        self.focus = focus
        self.focus_indice = []

    def key_shift_focus(self, direction):
        """Function that shifts focus on arrow key press"""
        # 1 = left, 2 = right, 3 = up, 4 = down.
        offsets = [-1, 1, -9, 9]
        focus_offset = offsets[direction-1]
        tmp_focus = self.get_focus()
        shifted = False
        while not shifted:
            if tmp_focus in self.focus_indice and tmp_focus != self.get_focus():
                self.set_focus_index(tmp_focus)
                shifted = True
            elif tmp_focus + focus_offset < 0 or tmp_focus + focus_offset >= len(self.grid_str):
                break
            elif direction_check(focus_offset, tmp_focus):
                break
            elif tmp_focus not in self.focus_indice:
                tmp_focus = tmp_focus + focus_offset
                continue
            else:
                tmp_focus = tmp_focus + focus_offset
        return shifted

    def get_char(self, index):
        """Function that returns char at position index"""
        return self.grid_str[index]

    def is_blank(self, pos):
        """Function that returns bool if the character at position pos is blank"""
        return self.grid_str[pos] == "_"

    def fill_at_focus(self, element):
        """Function that fills element at focus position"""
        tmp_list = list(self.grid_str)
        tmp_list[self.focus] = element
        self.grid_str = "".join(tmp_list)

    def init_grid(self):
        """Function that starts the puzzle generation."""
        self.grid_str = generate_puzzle()
        # for i in range(0, 81):
        #     self.grid_str = self.grid_str + "_"

    def is_focused(self, focus_pos):
        """Function that returns if the focus position(focus_pos) is the same as the focused block
            in the model."""
        return self.focus == focus_pos

    def set_focus_index(self, focus_pos):
        """Function that set focus index."""
        self.focus = int(focus_pos)

    def get_focus(self):
        """Function that returns focus index"""
        return self.focus

    def print_str(self):
        """Function that prints the grid in 9x9 form as a string of 9 characters in 9 lines."""
        for i in range(0, 9):
            print(self.grid_str[i * 9: i * 9 + 9])
        print()


    def get_char_at_focus(self):
        """Function that returns character at focus"""
        return self.grid_str[self.focus]

    def str_to_grid(self):
        """Function that converts the string into an array/list of size 9x9(ie arr[9][9])"""
        grid_main = [[0]*9 for _ in range(9)]
        for i in range(0, 9):
            for j in range(0, 9):
                grid_main[i][j] = self.grid_str[(i * 9) + j]
        return grid_main

    def is_valid_solution(self):
        """Function that returns True if the grid contains a fully filled valid pseudoku setup,
            False otherwise."""
        return (check(self.grid_str, "hori") and
                check(self.grid_str, "vert") and
                check(self.grid_str, "box"))

    def is_focusable(self, pos):
        """Function that returns a bool based on whether the position(pos) is focusable or not."""
        return pos in self.focus_indice

    def remove_boxes(self):
        """Function that removes boxes from the string at random, upto a maximum of 64 boxes removed"""
        dupe_list = list(self.grid_str)
        max_to_remove = random.randrange(20, 64)
        # print(max_to_remove)
        while max_to_remove > 0:
            remove_pos = random.randrange(0, len(dupe_list))
            if dupe_list[remove_pos] != "_":
                dupe_list[remove_pos] = "_"
                max_to_remove = max_to_remove - 1
                self.focus_indice.append(remove_pos)
        self.grid_str = "".join(dupe_list)

    def is_filled(self):
        """Function that returns bool when the string does not contain blanks("_")"""
        return not "_" in self.grid_str

def generate_puzzle():
    """Function that generates the puzzle. The algorithm is from this link
        https://gamedev.stackexchange.com/questions/56149/how-can-i-generate-sudoku-puzzles
        by a user named Yaling Zheng"""
    dupe_array = const.numbers_array[:]
    num_len = len(const.numbers_array)
    grid_main = [[0]*9 for _ in range(9)]
    counter = 0
    while num_len != 0:
        pop = random.randrange(0, num_len)
        grid_main[0][counter] = dupe_array[pop]
        dupe_array.pop(pop)
        num_len = num_len - 1
        counter = counter + 1
    for i in range(1, 9):
        grid_main[i] = grid_main[i - 1][:]
        if i % 3 == 0:
            shift_list(grid_main[i], 1)
        else:
            shift_list(grid_main[i], 3)
    final_list = "".join(str(item) for innerlist in grid_main for item in innerlist)
    return final_list

def get_box(grid_seq, offset):
    """Function that gets the 3x3 box from the position of the box(offset)"""
    box_row = []
    # Block 1
    block_pos = int(offset/3) * 27 + (offset % 3) * 3
    
    block_1 = grid_seq[block_pos: block_pos + 3]
    # Block 2
    block_2 = grid_seq[block_pos + 9: block_pos + 12]
    # Block 3
    block_3 = grid_seq[block_pos + 18: block_pos + 21]
    for i in range(0, 3):
        box_row.append(block_1[i])
        box_row.append(block_2[i])
        box_row.append(block_3[i])
    return box_row

def get_vert(grid_seq, offset):
    """Function that gets all vertical elements at index offset"""
    row_in_elements=[]
    for i in range(0,9):
        row_in_elements.append(grid_seq[i*9 + offset])
    return row_in_elements

def check(grid_seq, parse):
    """Function that checks all rows, columns and boxes for a valid solution."""
    satisfies = True
    numbers_arraystr = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for i in range(0, 9):
        row_in_elements = None
        if parse == "hori":
            row_in_elements = grid_seq[i*9: i*9 + 9]
        if parse == "vert":
            row_in_elements = get_vert(grid_seq, i)
        if parse == "box":
            row_in_elements = get_box(grid_seq, i)
        for element in row_in_elements:
            if element in numbers_arraystr:
                numbers_arraystr.remove(element)
            else:
                break
        if len(numbers_arraystr) == 0:
            numbers_arraystr = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        else:
            satisfies = False
            break
    return satisfies


def shift_list(grid_list, shift_amt):
    """Shifts the string to the left based on the generating algorithm by shift_amt"""
    for i in range(0, 9 - shift_amt):
        tmp = grid_list[i]
        grid_list[i] = grid_list[i - shift_amt]
        grid_list[i - shift_amt] = tmp

def direction_bool(focus_offset, focus_pos):
    """Bool check for direction_check()"""
    return ((focus_pos % 9 == 0 and focus_offset == -1) or
            (focus_pos %9 == 8 and focus_offset == 1))

def direction_check(focus_offset, focus_pos):
    """Keyboard handle function that ensures we dont go out of bounds"""
    return direction_bool(focus_offset, focus_pos)
