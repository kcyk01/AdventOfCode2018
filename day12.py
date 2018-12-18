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


def simulate(n: int) -> int:
    global first, last
    i = 0
    sequence = []
    while i < n:
        node = first
        while node:
            node.spread()
            node = node.right
        first.pad_left()
        last.pad_right()

        if n > 1000:
            # Look for patterns/cycles to skip simulation and use the cycle to predict the target result
            sequence.append(compute_result(first))
            cycle = find_cycle(sequence)
            if cycle > 0:
                # Add the cycle to skip remaining simulation
                return (n - i - 1) * cycle + compute_result(first)

        i += 1

    return compute_result(first)


def compute_result(start) -> int:
    s, node = 0, start
    while node:
        s += node.pos if node.state == '#' else 0
        node = node.right
    return s


def find_cycle(sequence: list) -> int:
    if len(sequence) > 100:
        # Sequence of at least 100 numbers, check the difference between the values
        first_deriv = [sequence[i] - sequence[i - 1] for i in range(1, len(sequence))]
        second_deriv = [first_deriv[i] - first_deriv[i - 1] for i in range(1, len(first_deriv))]
        if second_deriv[-50:] == [0] * 50:
            # Second derivative 0, constant rate of change between values
            return first_deriv[-1]
    return -1


def init(puzzle_input: str):
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


def day12a(puzzle_input: str) -> int:
    global first, last
    init(puzzle_input)
    return simulate(20)


def day12b(puzzle_input: str) -> int:
    global first, last
    init(puzzle_input)
    return simulate(50000000000)


if __name__ == '__main__':
    day12_input = get_input('day12.txt')
    print(day12a(day12_input))
    print(day12b(day12_input))
