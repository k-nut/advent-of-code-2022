import re
from collections import deque
from dataclasses import dataclass

from helpers import get_data


@dataclass
class Move:
    move_from: int
    move_to: int
    count: int

    @staticmethod
    def from_string(string: str):
        pattern = r"move (\d+) from (\d+) to (\d+)"
        count, move_from, move_to = [int(p) for p in re.match(pattern, string).groups()]
        return Move(move_from, move_to, count)


@dataclass
class Field:
    stacks: list[deque]

    @staticmethod
    def from_lines(lines: list[str]):
        slots = [int(n) for n in [line.strip() for line in lines[-1].split(" ")] if n]
        size = slots[-1]
        stacks = [deque() for _ in range(size)]
        for line in reversed(lines[:-1]):
            for index in range(size):
                column = (index * 4) + 1
                try:
                    value = line[column].strip()
                    if value:
                        stacks[index].append(value)
                except IndexError:
                    pass
        return Field(stacks)

    def apply_move(self, move: Move):
        for i in range(move.count):
            self.stacks[move.move_to - 1].append(self.stacks[move.move_from - 1].pop())

    def apply_multi_move(self, move: Move):
        values = []
        for i in range(move.count):
            values.append(self.stacks[move.move_from - 1].pop())
        for value in reversed(values):
            self.stacks[move.move_to - 1].append(value)


def day_4():
    # data = get_data(5, "example")
    data = get_data(5)

    lines = [line.strip() for line in data]
    sep = lines.index("")

    field_lines, move_lines = data[:sep], lines[(sep + 1) :]
    field = Field.from_lines(field_lines)
    moves = [Move.from_string(line) for line in move_lines]

    for move in moves:
        field.apply_move(move)
    print("Part 1: ", "".join([stack[-1] for stack in field.stacks]))

    field2 = Field.from_lines(field_lines)
    for move in moves:
        field2.apply_multi_move(move)

    print("Part 2: ", "".join([stack[-1] for stack in field2.stacks]))


if __name__ == "__main__":
    day_4()
