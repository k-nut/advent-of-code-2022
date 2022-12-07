import operator
import string
from dataclasses import dataclass

from helpers import chunk_list, get_data


@dataclass
class Item:
    value: str

    @property
    def priority(self):
        return operator.indexOf(string.ascii_letters, self.value) + 1


@dataclass
class Rucksack:
    left_compartment: str
    right_compartment: str

    @staticmethod
    def from_line(line: str):
        clean = line.strip()
        half = int(len(clean) / 2)
        left, right = clean[:half], clean[half:]
        return Rucksack(left_compartment=left, right_compartment=right)

    @property
    def shared_items(self):
        return set(self.left_compartment).intersection(set(self.right_compartment))

    @property
    def shared_items_priority(self):
        return sum([Item(item).priority for item in self.shared_items])

    @property
    def all_items(self):
        return set([*self.left_compartment, *self.right_compartment])


@dataclass
class Group:
    rucksacks: list[Rucksack]

    @property
    def shared_item(self):
        return (
            self.rucksacks[0].all_items
            & self.rucksacks[1].all_items
            & self.rucksacks[2].all_items
        )

    @property
    def shared_item_priority(self):
        return Item(self.shared_item.pop()).priority


def day_3():
    # data = get_data(3, "example")
    data = get_data(3)
    rucksacks = [Rucksack.from_line(line) for line in data]
    print("Part 1: ", sum(r.shared_items_priority for r in rucksacks))

    groups = [Group(chunk) for chunk in chunk_list(rucksacks, 3)]
    print("Part 2: ", sum(g.shared_item_priority for g in groups))


if __name__ == "__main__":
    day_3()
