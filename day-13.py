import json
from functools import cmp_to_key
from itertools import zip_longest
from typing import Union

from helpers import get_data, split_at


def compare(left: Union[int, list[int]], right: Union[int, list[int]]):
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return True
        if left > right:
            return False
    elif isinstance(left, list) and isinstance(right, list):
        for new_left, new_right in zip_longest(left, right):
            if new_left is None:
                # This means that the left list was shorter
                return True
            if new_right is None:
                return False
            result = compare(new_left, new_right)
            if result is not None:
                return result
    elif isinstance(left, int) and isinstance(right, list):
        return compare([left], right)
    elif isinstance(left, list) and isinstance(right, int):
        return compare(left, [right])
    else:
        raise Exception("Not sure how to handle", left, right)


def day_13():
    # data = get_data(13, "example")
    data = get_data(13)
    pairs = split_at([l.strip() for l in data], "")

    total = 0
    for i, p in enumerate(pairs):
        left, right = [json.loads(part) for part in (p[0], p[1])]
        if compare(left, right):
            total += i + 1

    print("Part 1: ", total)

    separators = [[[2]], [[6]]]
    parts = [l.strip() for l in data]
    all_lines = [json.loads(line) for line in parts if line]
    all_lines += separators

    def compare_signals(x, y):
        return -1 if compare(x, y) else 1

    product = 1
    for i, line in enumerate(sorted(all_lines, key=cmp_to_key(compare_signals))):
        if line in separators:
            product *= i + 1
    print("Part 2: ", product)


if __name__ == "__main__":
    day_13()
