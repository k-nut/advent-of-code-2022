from dataclasses import dataclass

from helpers import get_data

# from typing import Self



@dataclass
class SectionRange:
    min: int
    max: int

    @staticmethod
    def from_string(string: str):
        min, max = [int(part) for part in string.split("-")]
        return SectionRange(min, max)

    def contains(self, other):
        return self.min <= other.min and self.max >= other.max

    def overlaps(self, other):
        return other.min <= self.min <= other.max or self.min <= other.min <= self.max


@dataclass
class Pair:
    first: SectionRange
    second: SectionRange

    @staticmethod
    def from_line(line: str):
        first, second = line.strip().split(",")
        return Pair(SectionRange.from_string(first), SectionRange.from_string(second))

    @property
    def has_full_overlap(self):
        return self.first.contains(self.second) or self.second.contains(self.first)

    @property
    def has_overlap(self):
        return self.first.overlaps(self.second)


def day_4():
    # data = get_data(4, "example")
    data = get_data(4)
    pairs = [Pair.from_line(line) for line in data]

    print("Part 1: ", sum(1 for p in pairs if p.has_full_overlap))
    print("Part 2: ", sum(1 for p in pairs if p.has_overlap))


if __name__ == "__main__":
    day_4()
