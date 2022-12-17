import bisect
import re
from collections import namedtuple

from helpers import get_data

Range = namedtuple("Range", ("min", "max"))


def range_key(r: Range):
    return r.min, r.max


class RangeGroup:
    def __init__(self):
        self.ranges = []

    def merge_intervals(self):
        result = [self.ranges[0]]

        for r in self.ranges[1:]:
            last = result[-1]
            if last.min <= r.min <= last.max:
                result[-1] = Range(last.min, max(last.max, r.max))
            elif last.max == (r.min - 1):
                result[-1] = Range(last.min, max(last.max, r.max))
            else:
                result.append(r)
        self.ranges = result

    def add_range(self, new_range: Range):
        bisect.insort(self.ranges, new_range, key=range_key)
        self.merge_intervals()

    def covers(self, start, end):
        for range in self.ranges:
            if range.min <= start and range.max >= end:
                return True
        return False


def day_15():
    # data = get_data(15, "example")
    # target_line = 10
    # size = 20

    data = get_data(15)
    target_line = 2000000
    size = 4_000_000

    filled_spots = set()
    beacon_xs = set()
    for line in data:
        sensor_x, sensor_y, beacon_x, beacon_y = [int(n) for n in re.findall(r'-?\d+', line)]
        radius = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)

        target_distance_y = abs(target_line - sensor_y)
        range_in_line = max(radius - target_distance_y, 0)
        start = sensor_x - range_in_line
        end = sensor_x + range_in_line

        if beacon_y == target_line:
            beacon_xs.add(beacon_x)
        filled_spots.update(range(start, end + 1))

    print("Part 1: ", len(filled_spots - beacon_xs))

    candidates = {i: RangeGroup() for i in range(size + 1)}
    for line in data:
        sensor_x, sensor_y, beacon_x, beacon_y = [int(n) for n in re.findall(r'-?\d+', line)]
        radius = abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)
        print(line)

        current_keys = list(candidates.keys())
        for target_line in current_keys:
            target_distance_y = abs(target_line - sensor_y)
            range_in_line = radius - target_distance_y
            if range_in_line < 0:
                continue
            start = sensor_x - range_in_line
            end = sensor_x + range_in_line
            candidates[target_line].add_range(Range(start, end))
            if candidates[target_line].covers(0, size):
                candidates.pop(target_line)

    y_keys = list(candidates.keys())
    assert len(y_keys) == 1
    ranges = candidates[y_keys[0]].ranges
    assert len(ranges) == 2
    assert ranges[0].max + 1 == ranges[1].min - 1
    y_coordinate = y_keys[0]
    x_coordinate = ranges[0].max + 1
    print("Part 2: ", x_coordinate * 4000000 + y_coordinate)


if __name__ == "__main__":
    day_15()
