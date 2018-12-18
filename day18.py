from utils import get_input
from collections import defaultdict

terrain = {}
max_x, max_y = -1, -1


class Point:
    def __init__(self, x: int, y: int, initial: str):
        self.x = x
        self.y = y
        self.state = initial
        self.next = self.state

    def compute_next(self):
        adj = Point.get_adjacent(self.x, self.y)
        if self.state == '.' and adj.count('|') >= 3:
            self.next = '|'
        if self.state == '|' and adj.count('#') >= 3:
            self.next = '#'
        if self.state == '#' and ('#' not in adj or '|' not in adj):
            self.next = '.'

    def update(self):
        self.state = self.next

    @staticmethod
    def get_adjacent(x: int, y: int) -> str:
        global terrain
        adj = [
            (x - 1, y - 1),  # up left
            (x, y - 1),      # up
            (x + 1, y - 1),  # up right
            (x - 1, y),      # left
            (x + 1, y),      # right
            (x - 1, y + 1),  # down left
            (x, y + 1),      # down
            (x + 1, y + 1)   # down right
        ]
        return ''.join([terrain[p].state for p in adj if p in terrain])


def simulate(n: int):
    global terrain
    pattern = defaultdict(list)
    i = 0
    while i < n:
        for point in terrain.values():
            point.compute_next()
        for point in terrain.values():
            point.update()

        if n > 1000:
            # Look for patterns/cycles to skip simulation and use the cycle to predict the target result
            cycle = find_cycle(pattern, i, compute_product())
            if cycle > 0:
                # Set to end at nearest cycle equivalent to the target 'n'
                n = i + (n % cycle - i % cycle)

        i += 1


def compute_product():
    global terrain
    wooded = len([point for point in terrain.values() if point.state == '|'])
    lumberyard = len([point for point in terrain.values() if point.state == '#'])
    return wooded * lumberyard


def find_cycle(pattern: dict, i: int, product: int) -> int:
    pos = pattern[product]
    pos.append(i)
    if len(pos) > 5:
        # Target number has been seen at least 5 times, check the difference between the indices
        first_deriv = [pos[i] - pos[i - 1] for i in range(1, len(pos))]
        second_deriv = [first_deriv[i] - first_deriv[i - 1] for i in range(1, len(first_deriv))]
        if second_deriv[-3:] == [0] * 3:
            # Second derivative 0, constant rate of change between indices
            return first_deriv[-1]

    return -1


def day18a(puzzle_input: str) -> int:
    global terrain, max_x, max_y
    for y, line in enumerate(puzzle_input.strip().split('\n')):
        for x, c in enumerate(line):
            terrain[x, y] = Point(x, y, c)
            max_x = x
        max_y = y
    simulate(10)
    return compute_product()


def day18b(puzzle_input: str) -> int:
    global terrain, max_x, max_y
    for y, line in enumerate(puzzle_input.strip().split('\n')):
        for x, c in enumerate(line):
            terrain[x, y] = Point(x, y, c)

    simulate(1000000000)
    return compute_product()


def debug():
    global terrain, max_x, max_y
    temp_terrain = [['.' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for pos, point in terrain.items():
        temp_terrain[pos[1]][pos[0]] = point.state
    for row in temp_terrain:
        print(''.join(row))
    print()


if __name__ == '__main__':
    day18_input = get_input('day18.txt')
    print(day18a(day18_input))
    print(day18b(day18_input))
