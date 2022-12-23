from collections import defaultdict
from copy import copy

from helpers import get_data


def move(p1, p2):
    return p1[0] + p2[0], p1[1] + p2[1]


def print_field(positions):
    xs = [p[0] for p in positions]
    ys = [p[1] for p in positions]

    for y in range(min(ys), max(ys) + 1):
        for x in range(min(xs), max(xs) + 1):
            if (x, y) in positions:
                print("#", end="")
            else:
                print(".", end="")
        print()

def day_23():
    # data = get_data(23, "example-2")
    # data = get_data(23, "example")
    data = get_data(23)

    positions = set()
    for y, line in enumerate(data):
        for x, field in enumerate(line.strip()):
            if field == '#':
                positions.add((x, y))

    proposals = defaultdict(list)

    def get_next_position(position, index):
        directions = [
            {"move": (0, -1), "checks": [(-1, -1), (0, -1), (1, -1)]},  # N
            {"move": (0, 1), "checks": [(-1, 1), (0, 1), (1, 1)]},  # S
            {"move": (-1, 0), "checks": [(-1, -1), (-1, 0), (-1, 1)]},  # W
            {"move": (1, 0), "checks": [(1, -1), (1, 0), (1, 1)]},  # E
        ]
        neighbors = [(-1, -1), (-1, 0), (-1, 1),
                     (0, -1),           (0, 1),
                     (1, -1), (1, 0),   (1, 1)]
        if all(move(position, d) not in positions for d in neighbors):
            return None

        for direction in [*directions[(index % 4):], *directions[:(index % 4)]]:
            if all(move(position, d) not in positions for d in direction["checks"]):
                return position[0] + direction["move"][0], position[1] + direction["move"][1]

    positions_10 = set()
    for i in range(1_000_000_000):
        for elf in positions:
            if step := get_next_position(elf, i):
                proposals[step].append(elf)

        if len(proposals.keys()) == 0:
            print("Part 2:", i + 1)
            break
        for position, candidates in proposals.items():
            if len(candidates) == 1:
                positions.remove(candidates[0])
                positions.add(position)
        proposals = defaultdict(list)
        if i == 9:
            positions_10 = copy(positions)

    xs = [p[0] for p in positions_10]
    ys = [p[1] for p in positions_10]

    print("Part 1:", (max(xs) - min(xs) + 1) * (max(ys) - min(ys) + 1) - len(positions_10))


if __name__ == "__main__":
    day_23()
