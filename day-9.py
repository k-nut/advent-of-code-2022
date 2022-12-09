import math
from dataclasses import dataclass

from helpers import get_data

@dataclass
class Point:
    x: int
    y: int


@dataclass
class Field:
    parts: list[Point]
    tail_positions: set
    step = 0

    def __init__(self, length):
        self.parts = [Point(0, 0) for _ in range(length)]
        self.tail_positions = {(0,0)}


    @property
    def headPosition(self):
        return self.parts[0]

    @property
    def tailPosition(self):
        return self.parts[-1]

    def move_head(self, direction):
        head = self.parts[0]
        match direction:
            case 'U':
                head.y += 1
            case 'D':
                head.y -= 1
            case 'L':
                head.x -= 1
            case 'R':
                head.x += 1
        self.move_tail()

        # print(self.print())
        # with open(f"{str(self.step).zfill(5)}.txt", "w") as outfile:
        #     outfile.write(f"{self.step}\n{self.print()}")
        self.step += 1

    def move_tail(self):
        for i in range(1, len(self.parts)):
            previous = self.parts[i-1]
            next = self.parts[i]

            delta_x = previous.x - next.x
            delta_y = previous.y - next.y

            if abs(delta_x) < 2 and abs(delta_y) < 2:
                return

            if abs(delta_x) > 0 and abs(delta_y) > 0:
                # Handle a diagonal move
                next.x += math.copysign(1, delta_x)
                next.y += math.copysign(1, delta_y)
            else:
                if delta_x:
                    next.x += math.copysign(1, delta_x)
                if delta_y:
                    next.y += math.copysign(1, delta_y)

        self.tail_positions.add((self.tailPosition.x, self.tailPosition.y))

    def print(self):
        rows = []

        field_min = 0
        field_max = 6

        for y in range(field_min, field_max, 1):
            row = []
            for x in range(field_min, field_max, 1):
                if self.headPosition.x == x and self.headPosition.y == y:
                    row.append('H')
                    continue
                found = False
                for i in range(1, 10):
                    part = self.parts[i]
                    if part.x == x and part.y == y:
                        found = True
                        row.append(str(i))
                        break
                # if (x, y) in self.tail_positions:
                #     row.append('#')
                if not found:
                    row.append('.')
            rows.append(row)
        res = ""
        for row in reversed(rows):
            res += "".join(row) + "\n"
        return res


def day_9():
    # data = get_data(9, "example")
    # data = get_data(9, "example-2")
    data = get_data(9)

    moves = []
    for line in data:
        direction, steps = line.strip().split(" ")
        moves += [direction] * int(steps)

    field = Field(2)
    for move in moves:
        field.move_head(move)

    print("Part 1: ", len(field.tail_positions))

    field_2 = Field(10)
    for move in moves:
        field_2.move_head(move)

    print("Part 2: ", len(field_2.tail_positions))

if __name__ == "__main__":
    day_9()
