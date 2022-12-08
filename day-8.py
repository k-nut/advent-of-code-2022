import math
from collections import defaultdict
from dataclasses import dataclass

from helpers import get_data


@dataclass
class GridValue:
    value: int
    x: int
    y: int


@dataclass
class Grid:
    values: dict

    def __init__(self):
        self.values = defaultdict(lambda: defaultdict(GridValue))

    @property
    def cells(self):
        for row in self.values.values():
            for value in row.values():
                yield value

    def set(self, x, y, value):
        self.values[y][x] = GridValue(x=x, y=y, value=value)

    def get(self, x, y):
        return self.values.get(y, {}).get(x)

    def right(self, x, y):
        return self.get(x + 1, y)

    def left(self, x, y):
        return self.get(x - 1, y)

    def top(self, x, y):
        return self.get(x, y - 1)

    def bottom(self, x, y):
        return self.get(x, y + 1)

    def is_visible(self, x, y):
        for direction in ["left", "right", "top", "bottom"]:
            is_visible = self.is_direction_visible(x, y, direction)
            if is_visible:
                return True
        return False

    def is_direction_visible(self, x, y, direction):
        height = self.get(x, y).value
        for neighbor in self.direction_neighbors(x, y, direction):
            if neighbor.value >= height:
                return False
        return True

    def direction_scenic_score(self, x, y, direction):
        height = self.get(x, y).value
        count = 0
        for neighbor in self.direction_neighbors(x, y, direction):
            count += 1
            if neighbor.value >= height:
                break
        return count

    def direction_neighbors(self, x, y, direction):
        neighbor = getattr(self, direction)
        value = neighbor(x, y)
        while value:
            yield value
            value = neighbor(value.x, value.y)

    def scenic_score(self, x, y):
        directions = ["left", "right", "top", "bottom"]
        return math.prod(self.direction_scenic_score(x, y, d) for d in directions)


def day_8():
    # data = get_data(8, "example")
    data = get_data(8)

    grid = Grid()
    for y, line in enumerate(data):
        for x, value in enumerate(line.strip()):
            grid.set(x, y, int(value))

    print("Part 1: ", sum(1 for cell in grid.cells if grid.is_visible(cell.x, cell.y)))
    print("Part 2: ", max(grid.scenic_score(cell.x, cell.y) for cell in grid.cells))


if __name__ == "__main__":
    day_8()
