import heapq
import math
from collections import defaultdict
from dataclasses import dataclass

from helpers import get_data, split_at


@dataclass
class GridValue:
    value: str
    x: int
    y: int


@dataclass
class Grid:
    values: dict
    DIRECTIONS = ["left", "right", "top", "bottom"]

    def __init__(self):
        self.values = defaultdict(lambda: defaultdict(GridValue))

    @property
    def cells(self):
        for row in self.values.values():
            for value in row.values():
                yield value

    def reachable_from(self, x, y):
        value = self.get(x, y).value
        neighbors = [getattr(self, direction)(x, y) for direction in self.DIRECTIONS]
        return [n for n in neighbors if n and ord(n.value) <= (ord(value) + 1)]

    def downwards_neighbors(self, x, y):
        current_height = self.get(x, y).value
        neighbors = [getattr(self, direction)(x, y) for direction in self.DIRECTIONS]
        return [n for n in neighbors if n and (ord(n.value) + 1) >= ord(current_height) ]

    def set(self, x, y, value):
        self.values[y][x] = GridValue(x=x, y=y, value=value)

    def get(self, x, y) -> GridValue:
        return self.values.get(y, {}).get(x)

    def right(self, x, y):
        return self.get(x + 1, y)

    def left(self, x, y):
        return self.get(x - 1, y)

    def top(self, x, y):
        return self.get(x, y - 1)

    def bottom(self, x, y):
        return self.get(x, y + 1)



# taken and adapted from:
# https://bradfieldcs.com/algos/graphs/dijkstras-algorithm/
def calculate_distances(graph, starting_vertex, get_candidates):
    distances = {starting_vertex: 0}

    pq = [(0, starting_vertex)]
    while len(pq) > 0:
        current_distance, current_vertex = heapq.heappop(pq)

        # Nodes can get added to the priority queue multiple times. We only
        # process a vertex the first time we remove it from the priority queue.
        if current_distance > distances.get(current_vertex, math.inf):
            continue

        for neighbor in graph.reachable_from(current_vertex[0], current_vertex[1]):
            coords = (neighbor.x, neighbor.y)
            distance = current_distance + 1

            # Only consider this new path if it's better than any path we've
            # already found.
            if distance < distances.get(coords, math.inf):
                distances[coords] = distance
                heapq.heappush(pq, (distance, coords))

    return distances


def calculate_distances_2(graph: Grid, starting_vertex):
    distances = {starting_vertex: 0}

    pq = [(0, starting_vertex)]
    while len(pq) > 0:
        current_distance, current_vertex = heapq.heappop(pq)

        if current_distance > distances.get(current_vertex, math.inf):
            continue

        for neighbor in graph.downwards_neighbors(current_vertex[0], current_vertex[1]):
            coords = (neighbor.x, neighbor.y)
            distance = current_distance + 1

            if distance < distances.get(coords, math.inf):
                distances[coords] = distance
                heapq.heappush(pq, (distance, coords))

    return distances


def day_12():
    # data = get_data(12, "example")
    data = get_data(12)

    grid = Grid()
    start = (0, 0)
    end = (0, 0)
    for y, line in enumerate(data):
        for x, value in enumerate(line.strip()):
            if value == 'S':
                start = (x, y)
                value = 'a'
            if value == 'E':
                end = (x, y)
                value = 'z'
            grid.set(x, y, value)

    distances = calculate_distances(grid, start)
    print("Part 1: ", distances[end])

    distances2 = calculate_distances_2(grid, end)
    min_distance = math.inf
    count = 0
    for (x,y), value in distances2.items():
        if grid.get(x, y).value == 'a':
            count += 1
            min_distance = min(min_distance, value)
    print("Part 2: ", min_distance)


if __name__ == "__main__":
    day_12()
