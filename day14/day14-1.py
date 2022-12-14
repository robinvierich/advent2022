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


    # add 2 here to pad sides
    grid_width = xmax - xmin + 1 + 2
    grid_height = ymax - ymin + 1

    # transform paths to make using Grid class possible
    # + 1 to pad sides
    paths = list(tuple((x - xmin + 1, y - ymin) for x, y in path) for path in input_paths) 

    grid = Grid(grid_width, grid_height, TileContents.Nothing)

    
    sand_start_loc = (input_sand_start_loc[0] - xmin + 1, input_sand_start_loc[1] - ymin)

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

    ybottom = grid.height

    sand_fell_below_bottom = False

    down_vec = GridDir.Down.get_dir_vector()
    left_vec = GridDir.Left.get_dir_vector()
    right_vec = GridDir.Right.get_dir_vector()

    valid_movement_vecs = [down_vec, v_add(down_vec, left_vec), v_add(down_vec, right_vec)]


    num_sand_particles = 0


    while not sand_fell_below_bottom:

        num_sand_particles += 1
        sand_loc = sand_start_loc

        i_move_vec = 0

        while i_move_vec < len(valid_movement_vecs):

            move_vec = valid_movement_vecs[i_move_vec]
            next_loc = v_add(sand_loc, move_vec)

            if next_loc[1] >= ybottom:
                sand_fell_below_bottom = True
                break

            can_move = grid.is_valid_loc(*next_loc) and grid.get_tile(*next_loc) == TileContents.Nothing

            if can_move:
                if sand_loc != sand_start_loc:
                    grid.set_tile(*sand_loc, TileContents.Nothing)

                grid.set_tile(*next_loc, TileContents.Sand)

                sand_loc = next_loc
                i_move_vec = 0
            else:
                i_move_vec += 1
            
          
        
        #print (grid)
    
    # final sand particle doesn't count, it fell below the bottom
    num_sand_particles -= 1
    
    print ("num sand particles: {}".format(num_sand_particles))


        


           
        



    
        

          

    
if __name__ == "__main__":
    main()