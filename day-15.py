import math
import re
from collections import defaultdict, namedtuple
from dataclasses import dataclass
from time import sleep

from helpers import get_data

Point = namedtuple("Point", ("x", "y"))


def day_15():
    # data = get_data(15, "example")
    data = get_data(15)

    target_line = 2000000
    # target_line = 10
    filled_spots = set()
    beacon_xs = set()
    for line in data:
        sensor_x, sensor_y, beacon_x, beacon_y = [int(n) for n in re.findall(r'-?\d+', line)]
        radius = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)

        target_distance_y = abs(target_line - sensor_y)
        spots_in_line = max(radius - target_distance_y, 0)
        start = sensor_x - spots_in_line
        end = sensor_x + spots_in_line

        if beacon_y == target_line:
            beacon_xs.add(beacon_x)
        filled_spots.update(range(start, end + 1))

    print("Part 1: ", len(filled_spots - beacon_xs))


if __name__ == "__main__":
    day_15()
