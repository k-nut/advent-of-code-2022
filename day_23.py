from collections import defaultdict

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

    for i in range(10):
        for elf in positions:
            step = get_next_position(elf, i)
            if step:
                proposals[step].append(elf)

        for position, candidates in proposals.items():
            if len(candidates) == 1:
                positions.remove(candidates[0])
                positions.add(position)
        proposals = defaultdict(list)
        # print(f"After round {i+1}")
        # print_field(positions)

    xs = [p[0] for p in positions]
    ys = [p[1] for p in positions]

    print("Part 1:", (max(xs) - min(xs) + 1) * (max(ys) - min(ys) + 1) - len(positions))


if __name__ == "__main__":
    day_23()
