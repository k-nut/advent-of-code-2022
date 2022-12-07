def day_1():
    with open("./data/1-1.txt") as infile:
        data = infile.readlines()
    calories = [0]
    for line in data:
        value = line.strip()
        if value == "":
            calories.append(0)
        else:
            calories[-1] += int(value)

    print(calories)

    print("Part 1: ", max(calories))

    print("Part 2: ", sum(sorted(calories)[-3:]))


if __name__ == "__main__":
    day_1()
