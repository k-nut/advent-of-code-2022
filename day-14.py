from collections import defaultdict, namedtuple
from dataclasses import dataclass
from time import sleep

from helpers import get_data

Point = namedtuple("Point", ("x", "y"))


@dataclass
class Grid:
    def __init__(self):
        self.values = defaultdict(lambda: defaultdict(str))

    def set(self, x: int, y: int, value: str):
        self.values[y][x] = value

    def get(self, point: Point):
        return self.values.get(point.y, {}).get(point.x)

    def set_from_lines(self, data: list[str]):
        for line in data:
            parts = [to_coords(c) for c in line.strip().split(' -> ')]
            for start, end in zip(parts, parts[1:]):
                coords = get_line_coordinates(start, end)
                for x, y in coords:
                    self.set(x, y, '#')

    def print(self):
        import os
        os.system('clear')
        max_y = max(self.values.keys()) + 2
        min_y = min(0, min(self.values.keys()))
        min_x = min(min(row.keys()) for row in self.values.values())
        man_x = max(max(row.keys()) for row in self.values.values())
        for y in range(min_y, max_y + 1):
            print("".join(self.get(Point(x, y)) or '.' for x in range(min_x, man_x + 1)))

    def simulate(self):
        pos = Point(500, 0)
        max_y = max(self.values.keys())
        min_x = min(min(row.keys()) for row in self.values.values())
        count = 0
        while True:
            down_pos = Point(pos.x, pos.y + 1)
            down_left_pos = Point(pos.x - 1, pos.y + 1)
            down_right_pos = Point(pos.x + 1, pos.y + 1)
            if not self.get(down_pos):
                pos = down_pos
            elif not self.get(down_left_pos):
                pos = down_left_pos
            elif not self.get(down_right_pos):
                pos = down_right_pos
            else:
                self.set(pos.x, pos.y, 'o')
                count += 1
                pos = Point(500, 0)
            if pos.x < min_x or pos.y > max_y:
                return count

    def simulate_2(self):
        pos = Point(500, 0)
        max_y = max(self.values.keys())
        floor_y = max_y + 2
        count = 0
        while True:
            down_pos = Point(pos.x, pos.y + 1)
            down_left_pos = Point(pos.x - 1, pos.y + 1)
            down_right_pos = Point(pos.x + 1, pos.y + 1)
            could_fall = False
            for p in [down_pos, down_left_pos, down_right_pos]:
                if not self.get(p):
                    pos = p
                    could_fall = True
                if p.y + 1 == floor_y:
                    could_fall = False
            if pos.x == 500 and pos.y == 0:
                return count
            if not could_fall:
                self.set(pos.x, pos.y, 'o')
                count += 1
                pos = Point(500, 0)


def get_line_coordinates(start: Point, end: Point):
    start_x, start_y = start
    end_x, end_y = end
    if start_x == end_x:
        return [(start_x, y) for y in range(min(start_y, end_y), max(start_y, end_y) + 1)]
    if start_y == end_y:
        return [(x, start_y) for x in range(min(start_x, end_x), max(start_x, end_x) + 1)]


def to_coords(coord_str) -> Point:
    x, y = [int(c) for c in coord_str.split(",")]
    return Point(x, y)


def day_14():
    # data = get_data(14, "example")
    data = get_data(14)

    grid = Grid()
    grid.set_from_lines(data)
    print("Part 1: ", grid.simulate())

    grid_2 = Grid()
    grid_2.set_from_lines(data)
    print("Part 2: ", grid_2.simulate_2() + 1)


if __name__ == "__main__":
    day_14()
