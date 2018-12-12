import re

from utils import get_input

first, last = None, None


class Pot:
    rules = {}

    def __init__(self, i: int, c: str):
        self.pos = i
        self.state = c
        self.left = None
        self.right = None
        self.prev = self.state

    def __repr__(self):
        return self.state

    def pad_left(self):
        global first
        left = Pot(self.pos - 1, '.')
        self.left, left.right = left, self
        first = left

    def pad_right(self):
        global last
        right = Pot(self.pos + 1, '.')
        self.right, right.left = right, self
        last = right

    def spread(self):
        state_str = ''
        if self.left is None:
            state_str += '..'
        else:
            state_str += ('.' if self.left.left is None else self.left.left.prev) + self.left.prev
        state_str += self.state
        if self.right is None:
            state_str += '..'
        else:
            state_str += self.right.state + ('.' if self.right.right is None else self.right.right.state)
        self.prev = self.state
        self.state = Pot.rules[state_str] if state_str in Pot.rules else '.'


def day12a(puzzle_input: str) -> int:
    global first, last
    m = re.search(r'initial state: ([.#]+)', puzzle_input)
    start, node = None, None
    for i, c in enumerate(m.group(1)):
        if node is not None:
            node.right = Pot(i, c)
            node.right.left = node
            node = node.right
        else:
            node = Pot(i, c)
            first = node
            first.pad_left()
    last = node
    last.pad_right()

    rules = re.findall(r'([.#]+) => ([.#])', puzzle_input)
    for rule in rules:
        Pot.rules[rule[0]] = rule[1]

    simulate(20)
    return compute_result(first)


def simulate(n: int):
    global first, last
    for i in range(n):
        node = first
        while node:
            node.spread()
            node = node.right
        first.pad_left()
        last.pad_right()


def compute_result(start) -> int:
    s, node = 0, start
    while node:
        s += node.pos if node.state == '#' else 0
        node = node.right
    return s


def day12b(puzzle_input: str) -> int:
    global first, last
    # Simulate another 80 more generations
    simulate(80)

    # Pattern after about 100 generations
    return (50000000000 - 100) * 80 + compute_result(first)


if __name__ == '__main__':
    day12_input = get_input('day12.txt')
    print(day12a(day12_input))
    print(day12b(day12_input))
