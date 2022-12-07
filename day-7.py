import math
from dataclasses import dataclass
from typing import Optional, Union

from helpers import get_data


@dataclass
class File:
    name: str
    size: int


@dataclass
class Directory:
    name: str
    children: list[Union[File, "Directory"]]
    parent: Optional["Directory"]

    def add_directory(self, name: str):
        self.children.append(Directory(parent=self, name=name, children=[]))

    def get_child_directory(self, name: str):
        for child in self.children:
            if child.name == name:
                return child
        raise Exception(f"Directory not found: {name} in {self.name}")

    def add_file(self, name: str, size: int):
        self.children.append(File(name=name, size=size))

    def print(self, indent=0):
        print(" " * indent, self.name, f" ({self.size})")
        for child in self.children:
            if isinstance(child, File):
                print(" " * (indent + 2), child.name, child.size)
            else:
                child.print(indent + 2)

    @property
    def size(self):
        total = 0
        for child in self.children:
            total += child.size
        return total

    @property
    def directories(self):
        return [d for d in self.children if isinstance(d, Directory)]

    @property
    def part_1(self):
        total = self.size if self.size < 100000 else 0
        for child in self.directories:
            total += child.part_1
        return total

    def part_2(self, target_size, best):
        if self.size > target_size:
            new_best = min(best, self.size)
        else:
            new_best = best
        for child in self.directories:
            new_best = min(child.part_2(target_size, new_best), new_best)
        return new_best


def day_7():
    # data = get_data(7, "example")
    data = get_data(7)
    fs = Directory(name="<root>", children=[], parent=None)
    fs.add_directory("/")
    pointer = fs

    for line in data:
        line = line.strip()
        if line.startswith("$"):
            if "cd" in line:
                directory = line.split(" ")[-1]
                if directory == "..":
                    pointer = pointer.parent
                else:
                    pointer = pointer.get_child_directory(directory)
            elif "ls" in line:
                pass
            else:
                raise "unknown command"
        else:
            if line.startswith("dir"):
                pointer.add_directory(line.split(" ")[-1])
            else:
                size, name = line.split(" ")
                pointer.add_file(name, int(size))

    print("Part 1: ", fs.part_1)

    SIZE = 70000000
    TARGET = 30000000
    print("Part 2: ", fs.part_2(TARGET - (SIZE - fs.size), math.inf))


if __name__ == "__main__":
    day_7()
