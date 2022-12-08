import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.input_helper import InputType, read_input_lines
from common.grid import Grid, GridDir

def main():
    lines = read_input_lines(__file__, InputType.REAL_INPUT)

    grid_width = len(lines[0].strip())
    grid_height = len(lines)

    grid = Grid(grid_width, grid_height)

    for y, line in enumerate(lines):
        for x, tile in enumerate(line.strip()):
            grid.set_tile(x, y, int(tile))
    

    #row_maxes = max((tile for tile in grid.enumerate_row(row_y)) for row_y in range(grid.height))
    #col_maxes = max((tile for tile in grid.enumerate_col(col_y)) for col_y in range(grid.width))




    # walk each direction from perimeter
    # capture max as we walk

    # the perimeter is always visible from outside
    # num_visible_trees = 2 * grid_width + 2 * grid_height

    num_visible_trees = 0

    for col_x in range(grid.width):
        for row_y in range(grid.height):

            tree_height = grid.get_tile(col_x, row_y)

            for dir in GridDir.all_dirs:

                blocking_tree = False

                for x,y, other_height in grid.walk_in_direction(col_x, row_y, dir):
                    if other_height >= tree_height:
                        blocking_tree = True
                        break

                if not blocking_tree:
                    num_visible_trees += 1
                    break

    
    print("num visible trees {num}".format(num = num_visible_trees))



            


   


        
        

    print("Parsed Grid: \n{grid}".format(grid = grid))

    
if __name__ == "__main__":
    main()