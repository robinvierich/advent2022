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
    
    print("Parsed Grid: \n{grid}".format(grid = grid))

    #row_maxes = max((tile for tile in grid.enumerate_row(row_y)) for row_y in range(grid.height))
    #col_maxes = max((tile for tile in grid.enumerate_col(col_y)) for col_y in range(grid.width))




    # walk each direction from perimeter
    # capture max as we walk

    # the perimeter is always visible from outside
    # num_visible_trees = 2 * grid_width + 2 * grid_height

    num_visible_trees = 0

    max_tree_score = 0

    for col_x in range(grid.width):
        for row_y in range(grid.height):

            tree_height = grid.get_tile(col_x, row_y)

            tree_score = 1

            for dir in GridDir.all_dirs:

                visible_trees = 0

                for x,y, other_height in grid.walk_in_direction(col_x, row_y, dir):
                    visible_trees += 1
                    if other_height >= tree_height:
                        break
                
                # early-out
                if visible_trees == 0:
                    tree_score = 0
                    break

                tree_score *= visible_trees
            
            max_tree_score = max(tree_score, max_tree_score)


    
    print("max_tree_score {score}".format(score = max_tree_score))

        
        


    
if __name__ == "__main__":
    main()