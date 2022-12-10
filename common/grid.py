
from enum import Enum

class GridDir(Enum):
    Left = 1
    Up = 2
    Right = 3
    Down = 4




GridDir.all_dirs = [GridDir.Left, GridDir.Up, GridDir.Right, GridDir.Down]

def get_dir_vector(dir : GridDir) -> tuple:
    if dir == GridDir.Left:
        return (-1, 0)
    if dir == GridDir.Up:
        return (0, -1)
    if dir == GridDir.Right:
        return (1, 0)
    if dir == GridDir.Down:
        return (0, 1)

GridDir.get_dir_vector = get_dir_vector 

class Grid:

    def __init__(self, width, height, default_tile_val = None) -> None:
        self.data = [default_tile_val] * width * height

        self.stride = width

        self.width = width
        self.height = height
    
    def is_valid_loc(self, x, y):
        return (0 <= x and x < self.width) and (0 <= y and y < self.height)

    def get_tile_loc(self, i_tile):
        return i_tile % self.stride, i_tile // self.stride

    def get_tile_index(self, x, y):
        return y * self.stride + x

    def get_tile(self, x, y):
        i_tile = self.get_tile_index(x, y)
        return self.data[i_tile]

    def set_tile(self, x, y, tile):
        i_tile = self.get_tile_index(x, y)
        self.data[i_tile] = tile

        return tile

    def enumerate_row(self, row_y):
        for x in range(self.width):
            yield x, row_y, self.get_tile(x, row_y)

    def enumerate_col(self, col_x):
        for y in range(self.height):
            yield col_x, y, self.get_tile(col_x, y)

    def enumerate_grid(self):
        for y in range(self.height):
            yield self.enumerate_row(y)


    def get_next_loc_in_dir(self, x, y, dir):
        if dir == GridDir.Left:
            return x - 1, y
        if dir == GridDir.Up:
            return x, y + 1
        if dir == GridDir.Right:
            return x + 1, y
        if dir == GridDir.Down:
            return x, y - 1
    
    def walk_in_direction(self, x_start, y_start, dir, include_start_tile = False):

        x, y = x_start, y_start

        if not include_start_tile:
            x, y = self.get_next_loc_in_dir(x, y, dir)

        while self.is_valid_loc(x, y):
            yield x, y, self.get_tile(x, y)
            x, y = self.get_next_loc_in_dir(x, y, dir)

    

    def __str__(self) -> str:
        lines = []
        for y in range(self.height):
            lines.append(" ".join(str(self.get_tile(x, y)) for x in range(self.width)))

        return "\n".join(lines)
