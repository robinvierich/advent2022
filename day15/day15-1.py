import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from common.input_helper import InputType, read_input_lines

from common.grid import DynamicGrid, GridDir

from thirdparty.parse.parse import *


class Sensor:
    def __init__(self, closest_beacon_loc) -> None:
        self.closest_beacon_loc = closest_beacon_loc

    def __str__(self) -> str:
        return "S"
    
class Beacon:
    def __init__(self, closest_sensor_loc) -> None:
        self.closest_sensor_loc = closest_sensor_loc

    def __str__(self) -> str:
        return "B"

def manhatten_dist(pt1, pt2):
    return sum(abs(pt2i - pt1i) for pt1i, pt2i in zip(pt1, pt2))

def is_pt_covered_by_sensor(x, y, sensor_beacon_pairs):
    for sensor_loc, beacon_loc in sensor_beacon_pairs:
        sensor_beacon_dist = manhatten_dist(sensor_loc, beacon_loc)
        sensor_pt_dist = manhatten_dist(sensor_loc, (x, y))

        if sensor_pt_dist <= sensor_beacon_dist:
            return True
    
    return False

def get_x_ranges_covered_by_sensors_in_row(y, sensor_beacon_pairs):
    x_ranges = []
    for sensor_loc, beacon_loc in sensor_beacon_pairs:
        sensor_beacon_dist = manhatten_dist(sensor_loc, beacon_loc)

        sensor_x = sensor_loc[0]
        sensor_y = sensor_loc[1]

        sensor_y_to_edge = sensor_beacon_dist
        sensor_y_to_row = abs(sensor_y - y)

        y_overlap = sensor_y_to_edge - sensor_y_to_row

        if y_overlap >= 0:
            x_overlap_dist = y_overlap

            x_min, x_max = sensor_x - x_overlap_dist, sensor_x + x_overlap_dist  

            x_ranges.append((x_min, x_max))
        
    return x_ranges

        
def do_ranges_overlap(range1, range2):
    min1, max1 = range1
    min2, max2 = range2

    return (
           (min2 <= max1 <= max2)
        or (min1 <= max2 <= max1)
        #or (min2 <= min1 <= max2)
        #or (min1 <= min2 <= max1)
    )


def main():
    lines = read_input_lines(__file__, InputType.SAMPLE_INPUT)

    grid = DynamicGrid()

    format = "Sensor at x={sx:d}, y={sy:d}: closest beacon is at x={bx:d}, y={by:d}"

    sensor_beacon_pairs = []

    for line in lines:
        parsed_line = parse(format, line.strip())

        sensor_x, sensor_y = parsed_line['sx'], parsed_line['sy']
        beacon_x, beacon_y = parsed_line['bx'], parsed_line['by']

        sensor_loc = (sensor_x, sensor_y)
        beacon_loc = (beacon_x, beacon_y)

        print (sensor_loc)
        print (beacon_loc)

        s = Sensor(beacon_loc)
        b = Beacon(sensor_loc)

        grid.set_tile(sensor_x, sensor_y, s)
        grid.set_tile(beacon_x, beacon_y, b)

        sb_dist = manhatten_dist(sensor_loc, beacon_loc)

        #grid.extend_bounds_to_include_pt()

        sensor_beacon_pairs.append(((sensor_x, sensor_y), (beacon_x, beacon_y)))
    
    #print(grid)

    #y = 2000000
    y = 10

    num_covered_positions = 0

    x_ranges = get_x_ranges_covered_by_sensors_in_row(y, sensor_beacon_pairs)

    merged_ranges = [x_ranges[0]]

    i_curr = 0

    merged_any = True

    while merged_any:

        for x_range in x_ranges:
            merged_range = merged_ranges[i_curr]

            if do_ranges_overlap(merged_range, x_range):
                merged_range = x_range()

        





    merged_ranges = []
    merged_ranges.extend(x_ranges)

    merged_any = True

    while merged_any:
        merged_indices = []

        i_curr = 0

        for i in range(1, len(merged_ranges)):
            range1 = merged_ranges[i_curr]
            range2 = merged_ranges[i]

            if do_ranges_overlap(range1, range2):
                merged_range = min(range1[0], range2[0]), max(range1[1], range2[1])
                merged_ranges[i_curr] = merged_range
                merged_indices.append(i)
        

        merged_any = len(merged_indices) > 0

        for i in merged_indices:
            merged_ranges.pop(i)

    num_covered_positions = sum((x_max - x_min) + 1 for x_min, x_max in merged_ranges)

    visited = {}

    for sensor_loc, beacon_loc in sensor_beacon_pairs:
        for loc in (sensor_loc, beacon_loc):
            if loc not in visited and loc[1] == y:
                for x_min, x_max in x_ranges:
                    if x_min <= loc[1] <= x_max:
                        num_covered_positions -= 1
                        visited[loc] = True
                        break


    #for y in range(grid.ymin, grid.ymax + 1):
    # for x in range(grid.xmin, grid.xmax + 1):
    #     if is_pt_covered_by_sensor(x, y, sensor_beacon_pairs):
    #         if not grid.get_tile(x,y):
    #             num_covered_positions += 1
    #             grid.set_tile(x, y, "#")
    
    
    print(grid)
    print("num covered positions: {}".format(num_covered_positions))





    
if __name__ == "__main__":
    main()