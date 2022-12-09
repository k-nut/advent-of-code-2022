import math
from dataclasses import dataclass

from helpers import get_data

@dataclass
class Point:
    x: int
    y: int


@dataclass
class Field:
    headPosition: Point = Point(0, 0)
    tailPosition: Point = Point(0, 0)
    tail_positions = {(0, 0)}
    step = 0

    def move_head(self, direction):
        match direction:
            case 'U':
                self.headPosition.y += 1
            case 'D':
                self.headPosition.y -= 1
            case 'L':
                self.headPosition.x -= 1
            case 'R':
                self.headPosition.x += 1
        self.move_tail()

        # print(self.print())
        # with open(f"{str(self.step).zfill(5)}.txt", "w") as outfile:
        #     outfile.write(f"{self.step}\n{self.print()}")
        self.step += 1

    def move_tail(self):
        delta_x = self.headPosition.x - self.tailPosition.x
        delta_y = self.headPosition.y - self.tailPosition.y

        if abs(delta_x) < 2 and abs(delta_y) < 2:
            return

        if abs(delta_x) > 0 and abs(delta_y) > 0:
            # Handle a diagonal move
            self.tailPosition.x += math.copysign(1, delta_x)
            self.tailPosition.y += math.copysign(1, delta_y)
        else:
            if delta_x:
                self.tailPosition.x += math.copysign(1, delta_x)
            if delta_y:
                self.tailPosition.y += math.copysign(1, delta_y)

        self.tail_positions.add((self.tailPosition.x, self.tailPosition.y))

    def print(self):
        rows = []

        for y in range(0, 20, 1):
            row = []
            for x in range(0, 20, 1):
                if self.headPosition.x == x and self.headPosition.y == y:
                    row.append('H')
                elif self.tailPosition.x == x and self.tailPosition.y == y:
                    row.append('T')
                elif (x, y) in self.tail_positions:
                    row.append('#')
                else:
                    row.append('.')
            rows.append(row)
        res = ""
        for row in reversed(rows):
            res += "".join(row) + "\n"
        return res


def day_9():
    # data = get_data(9, "example")
    data = get_data(9)

    field = Field()
    moves = []
    for line in data:
        direction, steps = line.strip().split(" ")
        moves += [direction] * int(steps)

    for move in moves:
        field.move_head(move)

    print("Part 1: ", len(field.tail_positions))


if __name__ == "__main__":
    day_9()
