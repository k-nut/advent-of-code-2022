import math
import operator
import re
from functools import partial
from typing import Callable

from helpers import get_data, split_at


class Group:
    def __init__(self):
        self.monkeys = {}

    def add(self, monkey):
        monkey.monkey_group = self
        self.monkeys[monkey.number] = monkey

    def get(self, number):
        return self.monkeys[number]

    def run_round(self):
        for monkey in self.monkeys.values():
            monkey.inspect_and_throw()


class Monkey:
    number: int
    items: list[int]
    inspect_item: Callable
    divider: int
    true_target: int
    false_target: int
    monkey_group: Group

    def __init__(self, lines: list[str]):
        self.number = next(int(n) for n in re.findall(r'\d+', lines[0]))
        self.items = [int(n) for n in re.findall(r'\d+', lines[1])]
        self.inspect_item = Monkey._parse_operation(lines[2])
        self.divider = next(int(n) for n in re.findall(r'\d+', lines[3]))
        self.true_target = next(int(n) for n in re.findall(r'\d+', lines[4]))
        self.false_target = next(int(n) for n in re.findall(r'\d+', lines[5]))
        self.inspection_count = 0

    @staticmethod
    def _parse_operation(line: str):
        operator_1, operation, operator_2 = line.split(" = ")[1].split(" ")
        if operation not in ["+", "*"]:
            raise Exception("unkown operator")
        op = operator.add if operation == "+" else operator.mul
        if operator_2 == "old":
            return lambda x: op(x, x)
        return partial(op, int(operator_2))

    def inspect_and_throw(self):
        for item in self.items:
            self.inspection_count += 1
            new_worry = math.floor(self.inspect_item(item) / 3)
            target_number = self.true_target if new_worry % self.divider == 0 else self.false_target
            self.monkey_group.get(target_number).add(new_worry)
        self.items = []

    def add(self, worry: int):
        self.items.append(worry)


def day_11():
    # data = get_data(11, "example")
    data = get_data(11)

    group = Group()
    for lines in split_at([l.strip() for l in data], ""):
        group.add(Monkey(lines))

    for _ in range(20):
        group.run_round()

    *rest, second, first  = sorted(monkey.inspection_count for monkey in group.monkeys.values())
    print("Part 1: ", first * second)


if __name__ == "__main__":
    day_11()
