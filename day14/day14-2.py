import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.input_helper import InputType, read_input_lines

from common.grid import Grid, GridDir

import math

from enum import Enum

class TileContents(Enum):
    Nothing = 0,
    Rock = 1,
    Sand = 2,
    Spawner = 3

    def __str__(self) -> str:
        if self == TileContents.Nothing:
            return "."
        elif self == TileContents.Rock:
            return "#"
        elif self == TileContents.Sand:
            return "o"
        elif self == TileContents.Spawner:
            return "+"
        else:
            return super.__str__(self)



def sign(num):
    if num >= 0:
        return 1
    else:
        return -1


def v_add(v1, v2):
    return tuple(v1i + v2i for v1i, v2i in zip(v1, v2))


from PIL import Image, ImageTransform


def get_tile_color(tile):
    if tile == TileContents.Nothing:
        return (0, 0, 0)
    elif tile == TileContents.Rock:
        return (255, 0, 0)
    elif tile == TileContents.Sand:
        return (255, 128, 128)
    elif tile == TileContents.Spawner:
        return (0, 255, 0)

def create_grid_image(g: Grid):

    img = Image.new("RGB", (g.width, g.height), "black")
    pixels = img.load()

    for x, y, tile in g.enumerate_grid():
        pixels[x, y] = get_tile_color(tile)
    
    
    return img.resize((g.width * 32, g.height * 32), resample=Image.Resampling.NEAREST)
        


def main():
    in_lines = read_input_lines(__file__, InputType.REAL_INPUT)

    input_paths = []

    input_sand_start_loc = 500, 0

    xmin, ymin = input_sand_start_loc 
    xmax, ymax = input_sand_start_loc

    for in_line in in_lines:
        pointstrs = tuple(locstr.strip() for locstr in in_line.strip().split("->"))

        path = []

        for pointstr in pointstrs:
            point = tuple(int(coord) for coord in pointstr.strip().split(","))
            path.append(point)

            x, y = point

            xmin, ymin = min(x, xmin), min(y, ymin)
            xmax, ymax = max(x, xmax), max(y, ymax)
        
        input_paths.append(path)
    
    print(input_paths)
    print(xmin, ymin)
    print(xmax, ymax)



    floor_offset = 2
    # add 2 here to accomodate the infinite floor
    grid_height = ymax - ymin + 1 + (floor_offset - 1)

    width_padding = (grid_height)

    grid_width = xmax - xmin + 1 + width_padding * 2



    # transform paths to make using Grid class possible
    # + 1 to pad sides
    paths = list(tuple((x - xmin + width_padding, y - ymin) for x, y in path) for path in input_paths) 

    grid = Grid(grid_width, grid_height, TileContents.Nothing)

    
    sand_start_loc = (input_sand_start_loc[0] - xmin + width_padding, input_sand_start_loc[1] - ymin)

    grid.set_tile(*sand_start_loc, TileContents.Spawner)

    for path in paths:
        for i in range(1, len(path)):
            pt1 = path[i-1]
            pt2 = path[i]

            dx = pt2[0] - pt1[0]
            dy = pt2[1] - pt1[1]

            pt = pt1


            if dx != 0 and dy == 0:
                x_step = sign(dx)
                y = pt1[1]
                for x in range(pt1[0], pt2[0] + x_step, x_step):
                    grid.set_tile(x, y, TileContents.Rock)
                
            if dx == 0 and dy != 0:
                y_step = sign(dy)
                x = pt1[0]
                for y in range(pt1[1], pt2[1] + y_step, y_step):
                    grid.set_tile(x, y, TileContents.Rock)
    
    print(grid)

    images = []

    images.append(create_grid_image(grid))


    down_vec = GridDir.Down.get_dir_vector()
    left_vec = GridDir.Left.get_dir_vector()
    right_vec = GridDir.Right.get_dir_vector()

    valid_movement_vecs = [down_vec, v_add(down_vec, left_vec), v_add(down_vec, right_vec)]


    num_sand_particles = 0

    sand_pyramid_complete = False

    while not sand_pyramid_complete:


        sand_loc = sand_start_loc
        num_sand_particles += 1


        i_move_vec = 0

        moved = False

        while i_move_vec < len(valid_movement_vecs): 

            move_vec = valid_movement_vecs[i_move_vec]
            next_loc = v_add(sand_loc, move_vec)

            can_move = sand_loc[1] != (grid.height - 1) and grid.get_tile(*next_loc) == TileContents.Nothing

            if can_move:
                if sand_loc != sand_start_loc:
                    grid.set_tile(*sand_loc, TileContents.Nothing)

                grid.set_tile(*next_loc, TileContents.Sand)

                sand_loc = next_loc
                i_move_vec = 0
                moved = True
            else:
                i_move_vec += 1

        
        if not moved:
            sand_pyramid_complete = True
            
          
        
        #print (grid)
        #print ("")

        #images.append(create_grid_image(grid))
    

    print (grid)

    images.append(create_grid_image(grid))

    images[0].save('day-14-debug_image.gif', save_all=True, append_images=images[1:], optimize=False, duration=40)

   

    print ("num sand particles: {}".format(num_sand_particles))


          

    
if __name__ == "__main__":
    main()