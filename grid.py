class grid:
    
    def __init__(self, grid_str, focus = -1):
        self.grid_str = grid_str
        self.focus = focus
    
    def rotate_grid(self):
        print("in rotate - " + self.grid_str)

    def flip_grid(self):
        print("in flip - " + self.grid_str)

    def get_char(self, index):
        return self.grid_str[index]
    
    def is_blank(self, pos):
        return self.grid_str[pos] == "_"
    
    def fill_at_focus(self, element):
        tmp_list = list(self.grid_str)
        tmp_list[self.focus] = element
        self.grid_str = "".join(tmp_list)

    def init_grid(self):
        for i in range(0, 81):
            self.grid_str = self.grid_str + "_"

    def is_focused(self, focus_pos):
        return self.focus == focus_pos
    
    def set_focus_index(self, focus_pos):
        self.focus = int(focus_pos)
    
    def get_focus(self):
        return self.focus
    
    def print_str(self):
        print(self.grid_str)
    
    def get_char_at_focus(self):
        return self.grid_str[self.focus]
        