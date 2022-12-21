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


def main():
    lines = read_input_lines(__file__, InputType.SAMPLE_INPUT)

    grid = DynamicGrid()

    format = "Sensor at x={sx:d}, y={sy:d}: closest beacon is at x={bx:d}, y={by:d}"

    for line in lines:
        parsed_line = parse(format, line.strip())

        sensor_x, sensor_y = parsed_line['sx'], parsed_line['sy']
        beacon_x, beacon_y = parsed_line['bx'], parsed_line['by']

        print ((sensor_x, sensor_y))
        print ((beacon_x, beacon_y))

        s = Sensor((beacon_x, beacon_y))
        b = Beacon((sensor_x, sensor_y))

        grid.set_tile(sensor_x, sensor_y, s)
        grid.set_tile(beacon_x, beacon_y, b)
    
    print(grid)



    
if __name__ == "__main__":
    main()