from helpers import get_data


class Node:
    def __init__(self, value: int, start_position: int):
        self.value = value
        self.start_position = start_position
        self.next = None

    def after(self, n: int):
        pointer = self
        if n < 0:
            raise Exception(f"n must not be negative. Was {n}")
        for i in range(n):
            pointer = pointer.next
        return pointer

    def __repr__(self):
        return f"<Node value={self.value}, next={self.next.value}>"


def day_20():
    # data = get_data(20, "example")
    data = get_data(20)
    content = [int(n.strip()) for n in data]
    nodes = [Node(n, i) for i, n in enumerate(content)]

    for i, node in enumerate(nodes):
        node.next = nodes[(i + 1) % len(content)]

    for node in nodes:
        if node.value == 0:
            continue

        steps = node.value % (len(content) - 1)
        insertion_node = node.after(steps)
        buffer = insertion_node.next

        # print(f"{node.value} moves between {insertion_node.value} and {insertion_node.next.value}")

        prev = next(n for n in nodes if n.next == node)
        prev.next = node.next
        insertion_node.next = node
        node.next = buffer

    zero = next(n for n in nodes if n.value == 0)
    assert (zero == zero.after(len(content) - 1))

    print("Part 1: ", sum(zero.after(n).value for n in [1000, 2000, 3000]))


if __name__ == "__main__":
    day_20()
