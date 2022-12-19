from collections import namedtuple, defaultdict
from dataclasses import dataclass

from helpers import get_data

Point = namedtuple("Point", ("x", "y"))


@dataclass
class Grid:
    def __init__(self, moves: list[str]):
        self.values = defaultdict(lambda: defaultdict(str))
        self.max_x = 6
        self.current_shape_index = 0
        self.current_move_index = 0
        self._moves = moves
        self.move_gen = self._get_move()

    def set(self, point: Point, value: str):
        self.values[point.y][point.x] = value

    def get(self, point: Point):
        if point.x < 0 or point.x > self.max_x or point.y < 0:
            return 'W'
        return self.values.get(point.y, {}).get(point.x)

    def _get_move(self):
        while True:
            yield self._moves[self.current_move_index % len(self._moves)]
            self.current_move_index += 1
            yield 'DOWN'

    @property
    def height(self):
        return max(self.values.keys() or [-1])

    def add_brick(self, shape: list[Point]):
        i = 0
        offset = (2, self.height + 4)
        while True:
            pos = [Point(p.x + offset[0], p.y + offset[1]) for p in shape]
            move = next(self.move_gen)

            if move == 'DOWN':
                new_offset = (offset[0], offset[1] - 1)
                new_pos = [Point(p.x + new_offset[0], p.y + new_offset[1]) for p in shape]
                if any(self.get(p) for p in new_pos):
                    for p in pos:
                        self.set(p, '#')
                    break
                else:
                    offset = new_offset
            else:
                new_offset = (offset[0] + 1, offset[1]) if move == '>' else (offset[0] - 1, offset[1])
                new_pos = [Point(p.x + new_offset[0], p.y + new_offset[1]) for p in shape]
                found = any(self.get(p) for p in new_pos)
                if not found:
                    offset = new_offset
            i += 1

    def print(self):
        import os
        os.system('clear')
        max_y = self.height
        min_y = -1
        min_x = -1
        max_x = 7
        res = []
        for y in range(min_y, max_y + 1):
            res.append("".join(self.get(Point(x, y)) or '.' for x in range(min_x, max_x + 1)))
        for l in reversed(res):
            print(l)


h_bar = [(0, 0), (1, 0), (2, 0), (3, 0)]
plus = [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]
l = [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)]
v_bar = [(0, 0), (0, 1), (0, 2), (0, 3)]
square = [(0, 0), (1, 0), (0, 1), (1, 1)]


def day_17():
    # data = get_data(17, "example")
    data = get_data(17)

    grid = Grid(data[0].strip())
    shapes = [h_bar, plus, l, v_bar, square]
    for i in range(2022 + 1):
        shape = shapes[i % len(shapes)]
        grid.add_brick([Point(t[0], t[1]) for t in shape])
    print("Part 1: ", grid.height - 1)


if __name__ == "__main__":
    day_17()
