import operator
from functools import partial

from helpers import get_data


def noop(x):
    return x

def day_10():
    # data = get_data(10, "example")
    data = get_data(10, "example-2")
    # data = get_data(10)

    operations = []
    instructions = [line.strip() for line in data]
    for instruction in instructions:
        if instruction.startswith("noop"):
            operations.append(noop)
            continue
        operation, value = instruction.split(" ")
        operations.append(noop)
        operations.append(partial(operator.add, int(value)))

    x = 1
    total = 0
    for i, op in enumerate(operations):
        index = i + 1 # enumerate starts at 0 but we start counting at 1
        if (index -20) % 40 == 0:
            print(f"Index: {index}, x: {x}, product: {index * x}")
            total += index * x
        x = op(x)

    print("Part 1: ", total)

    x = 1
    for i, op in enumerate(operations):
        index = i
        # index = i + 1 # enumerate starts at 0 but we start counting at 1
        if index % 40 == 0:
            print()
        pos = index % 40
        if pos in [x-1, x, x+1]:
            print("#", end='')
        else:
            print(".", end="")
        x = op(x)

if __name__ == "__main__":
    day_10()
