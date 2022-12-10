import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.input_helper import InputType, read_input_lines

from common.grid import GridDir

import math


    



def parse_grid_dir(dirstr: str) -> GridDir:
    if dirstr == "L":
        return GridDir.Left
    elif dirstr == "U":
        return GridDir.Up
    elif dirstr == "R":
        return GridDir.Right
    elif dirstr == "D":
        return GridDir.Down


def vector_add(v1, v2):
    return tuple(v1i + v2i for v1i, v2i in zip(v1, v2))

def vector_mult(v1, v2):
    return tuple(v1i * v2i for v1i, v2i in zip(v1, v2))

def vector_sub(v1, v2):
    return tuple(v1i - v2i for v1i, v2i in zip(v1, v2))

def vector_mag_sqr(v):
    return sum(vi * vi for vi in v)

def vector_mag(v):
    return math.sqrt(vector_mag_sqr(v))


class Movement:
    def __init__(self, line: str) -> None:

        dirstr, diststr = line.strip().split(" ")

        self.dir = parse_grid_dir(dirstr)
        self.dist = int(diststr)



def get_grid_str(knot_positions, xmin = 0, xmax = 5, ymin = -4, ymax = 0):

    row_strs = []

    marked = set()

    for y in range (ymin, ymax + 1):

        row_chars = []

        for x in range(xmin, xmax + 1):
            for i, knot_pos in enumerate(knot_positions):
                if knot_pos in marked:
                    continue

                if knot_pos == (x, y):
                    if (i == 0):
                        row_chars.append("H")
                    else:
                        row_chars.append(str(i))
                    marked.add(knot_pos) 
            
            if not ((x, y) in marked):
                row_chars.append(".")
        
        row_strs.append("".join(row_chars))
    

    return "\n".join(row_strs)


def sign(x):
    if x >= 0:
        return 1
    else:
        return -1


def main():
    lines = read_input_lines(__file__, InputType.REAL_INPUT)

    movements = (Movement(line) for line in lines)

    knot_positions = [(0,0)] * 10

    visited_positions = set()
    visited_positions.add(knot_positions[-1])


    xmin, xmax = 0, 0
    ymin, ymax = 0, 0

    for movement in movements:
        dir_vec = GridDir.get_dir_vector(movement.dir)

        #print("== {movedir} {dist} ==".format(movedir = movement.dir, dist = movement.dist))

        for i in range(movement.dist):
            knot_positions[0] = vector_add(knot_positions[0], dir_vec)

            for i_knot in range(1, len(knot_positions)):
                i_headknot = i_knot - 1
                i_tailknot = i_knot

                headpos = knot_positions[i_headknot]
                tailpos = knot_positions[i_tailknot]


                xmin, xmax = min(xmin, headpos[0]), max(xmax, headpos[0])
                ymin, ymax = min(ymin, headpos[1]), max(ymax, headpos[1])

                tail_to_head = vector_sub(headpos, tailpos)

                tail_to_head_dist_sqr = vector_mag_sqr(tail_to_head)

                # if tail is far enough away to require movement
                if tail_to_head_dist_sqr >= (2 * 2):
                    tail_to_head_sign = tuple(sign(vi) for vi in tail_to_head)

                    # max cardinal dist change per step is 2
                    abs_tail_move_vec = math.ceil(abs(tail_to_head[0]) / 2), math.ceil(abs(tail_to_head[1]) / 2)

                    tail_move_vec = vector_mult(tail_to_head_sign, abs_tail_move_vec)

                    tailpos = vector_add(tailpos, tail_move_vec)
                    knot_positions[i_tailknot] = tailpos

                if i_tailknot == len(knot_positions) - 1:
                    visited_positions.add(tailpos)


            #print("\n{grid}".format(grid = get_grid_str(knot_positions)))
            #print("\n{grid}".format(grid = get_grid_str(headpos = headpos, tailpos = tailpos, xmin = xmin, xmax = xmax, ymin = ymin, ymax = ymax)))



    
    print("num visited positions: {num}".format(num = len(visited_positions)))

        










    
if __name__ == "__main__":
    main()