import re
from collections import defaultdict, namedtuple
from dataclasses import dataclass
from typing import Union

from helpers import get_data, split_at

Point = namedtuple("Point", ("x", "y"))


@dataclass
class Grid:
    def __init__(self):
        self.values = defaultdict(lambda: defaultdict(str))

    def set(self, point: Point, value: str):
        self.values[point.y][point.x] = value

    def get(self, point: Point) -> Union[None, str]:
        # if point.x < 0 or point.x > self.max_x or point.y < 0:
        #     return 'W'
        return self.values.get(point.y, {}).get(point.x)

    def x_bounds(self, y: int) -> (int, int):
        values = self.values[y].keys()
        return min(values), max(values)

    def y_bounds(self, x: int) -> (int, int):
        ys = []
        for y, values in self.values.items():
            if x in values:
                ys.append(y)
        return min(ys), max(ys)

    def next(self, point: Point, direction: str) -> (Point, str):
        direct, wrapped = self._get_options(point, direction)
        if value := self.get(direct):
            return direct, value
        return wrapped, self.get(wrapped)

    def _get_options(self, point: Point, direction: str) -> (Point, Point):
        match direction:
            case '>':
                return Point(point.x + 1, point.y), Point(self.x_bounds(point.y)[0], point.y)
            case 'v':
                return Point(point.x, point.y + 1), Point(point.x, self.y_bounds(point.x)[0])
            case '<':
                return Point(point.x - 1, point.y), Point(self.x_bounds(point.y)[1], point.y)
            case '^':
                return Point(point.x, point.y - 1), Point(point.x, self.y_bounds(point.x)[1])


def day_22():
    # data = get_data(22, "example")
    data = get_data(22)
    board, [path] = split_at(data, "\n")

    grid = Grid()
    for y, line in enumerate(board):
        for x, field in enumerate(line):
            if value := field.strip():
                grid.set(Point(x + 1, y + 1), value)

    position = Point(grid.x_bounds(1)[0], 1)
    directions = dict()
    direction = ">"
    direction_list = ['>', 'v', '<', '^']

    for operation in re.findall(r"\d+|[A-Z]+", path):
        if re.match(r"\d+", operation):
            for i in range(int(operation)):
                directions[position] = direction
                new_pos, value = grid.next(position, direction)
                if value == '#':
                    break
                position = new_pos
        else:
            addend = 1 if operation == 'R' else -1
            direction = direction_list[(direction_list.index(direction) + addend) % len(direction_list)]

    facings = {'>': 0, 'v': 1, '<': 2, '^': 3}
    result = position.y * 1000 + 4 * position.x + facings[direction]
    print("Part 1:", result)

    # for y in range(1, 13):
    #     for x in range(1, 17):
    #         p = Point(x, y)
    #         print(directions.get(p, grid.get(p) or ' '), end='')
    #     print()


if __name__ == "__main__":
    day_22()
