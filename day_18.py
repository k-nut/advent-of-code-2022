from helpers import get_data


def day_18():
    # data = get_data(18, "example")
    data = get_data(18)
    coords = set()
    for line in data:
        x,y,z = [int(n) for n in line.strip().split(',')]
        coords.add((x,y,z))

    count = 0
    for coord in coords:
        for pos in range(3):
            for direction in [-1, +1]:
                copy = list(coord)
                copy[pos] += direction
                if tuple(copy) not in coords:
                    count += 1

    print("Part 1: ", count)


if __name__ == "__main__":
    day_18()
