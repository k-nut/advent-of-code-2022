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

    def move(nodes):
        for node in nodes:
            steps = node.value % (len(content) - 1)
            if steps == 0:
                continue

            insertion_node = node.after(steps)
            buffer = insertion_node.next

            # print(f"{node.value} moves between {insertion_node.value} and {insertion_node.next.value}")

            prev = next(n for n in nodes if n.next == node)
            prev.next = node.next
            insertion_node.next = node
            node.next = buffer

    def part_1():
        nodes = [Node(n, i) for i, n in enumerate(content)]

        for i, node in enumerate(nodes):
            node.next = nodes[(i + 1) % len(content)]

        move(nodes)

        zero = next(n for n in nodes if n.value == 0)
        print("Part 1: ", sum(zero.after(n).value for n in [1000, 2000, 3000]))

    def part_2():
        key = 811589153
        nodes = [Node(n * key, i) for i, n in enumerate(content)]

        for i, node in enumerate(nodes):
            node.next = nodes[(i + 1) % len(content)]

        for _ in range(10):
            move(nodes)

        zero = next(n for n in nodes if n.value == 0)
        print("Part 2: ", sum(zero.after(n).value for n in [1000, 2000, 3000]))

    part_1()
    part_2()


if __name__ == "__main__":
    day_20()
