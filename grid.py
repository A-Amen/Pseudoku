class grid:
    
    def __init__(self, grid_str):
        self.grid_str = grid_str
    
    def rotate_grid(self):
        print("in rotate - " + self.grid_str)

    def flip_grid(self):
        print("in flip - " + self.grid_str)

    def get_char(self, index):
        return self.grid_str[index]
    
    def is_blank(self, pos):
        return self.grid_str[pos] == "_"
    
    def fill_at_pos(self, pos, element):
        self.grid_str[pos] = element
    def init_grid(self):
        for i in range(0, 81):
            self.grid_str = self.grid_str + "_"