import re

from utils import get_input

clay = set()
water = {}

min_y, max_y = 999999, -1
min_x, max_x = 999999, -1
start = (500, 0)

# Falling points is a stack, as we want to finish falling one fully before processing another falling point
falling_stack, falling_points = [], set()

# Spreading can be either a stack or a queue, using stack here
spread_stack, spread_points = [], set()


class Water:
    def __init__(self, source: (int, int), x: int, y: int):
        self.x = x
        self.y = y
        self.source = source
        self.descendants = []
        self.settled = False

    def __repr__(self):
        return '({}, {})'.format(self.x, self.y)

    def spread_horizontal(self):
        right_enclosed, left_enclosed = True, True
        descendant_source = (self.x, self.y) if self.y != self.source[1] else self.source

        # Horizontal expansion towards the right
        right, right_down = (self.x + 1, self.y), (self.x + 1, self.y + 1)
        while right not in clay:
            water[right] = Water(descendant_source, right[0], right[1])
            self.descendants.append(water[right])

            if right_down not in clay and right_down not in water:
                # Hole in the ground, not enclosed
                right_enclosed = False
                if right not in falling_points:
                    # Add this to the points to process for falling
                    falling_stack.append(water[right])
                    falling_points.add(right)
                break

            right, right_down = (right[0] + 1, right[1]), (right[0] + 1, right[1] + 1)

        # Horizontal expansion towards the left
        left, left_down = (self.x - 1, self.y), (self.x - 1, self.y + 1)
        while left not in clay:
            water[left] = Water(descendant_source, left[0], left[1])
            self.descendants.append(water[left])

            if left_down not in clay and left_down not in water:
                # Hole in the ground, not enclosed
                left_enclosed = False
                if left not in falling_points:
                    # Add this to the points to process for falling
                    falling_stack.append(water[left])
                    falling_points.add(left)
                break

            left, left_down = (left[0] - 1, left[1]), (left[0] - 1, left[1] + 1)

        # Both left and right hit clay, mark this and its descendants as settled
        if right_enclosed and left_enclosed:
            self.settled = True
            for d in self.descendants:
                d.settled = True
            # This layer has settled, tell the source to spread horizontally (adding to queue)
            if self.source not in spread_stack:
                spread_stack.append(water[self.source])
                spread_points.add(self.source)

    def fall(self):
        down = (self.x, self.y + 1)
        if down in clay or down in water and water[down].settled:
            # Cannot travel down, should spread horizontally if not already in the queue
            if (self.x, self.y) not in spread_stack:
                spread_stack.append(self)
                spread_points.add((self.x, self.y))
        elif down not in water and down[1] <= max_y:
            # Can travel down, add next point to stack of falling points
            descendant_source = (self.x, self.y) if self.y != self.source[1] else self.source
            water[down] = Water(descendant_source, down[0], down[1])
            if down not in falling_points:
                falling_stack.append(water[down])
                falling_points.add(down)


def simulate():
    global water, start, falling_stack, falling_points, spread_stack, spread_points

    # Initial water source
    water[start] = Water((500, 0), start[0], start[1])
    falling_stack.append(water[start])
    falling_points.add(start)

    # Main simulation, always process spreading before processing falling
    while len(falling_stack) > 0 or len(spread_stack) > 0:
        if len(spread_stack) > 0:
            w = spread_stack.pop()
            spread_points.remove((w.x, w.y))
            w.spread_horizontal()
        else:
            w = falling_stack.pop()
            falling_points.remove((w.x, w.y))
            w.fall()


def day17a(puzzle_input: str) -> int:
    global clay, water, min_y, max_y, min_x, max_x

    # Extract the clay, min and max from the puzzle input
    for line in puzzle_input.strip().split('\n'):
        m = re.search(r'([xy])=(\d+), [xy]=(\d+)\.\.(\d+)', line)
        if m.group(1) == 'x':
            x, ys = int(m.group(2)), (int(m.group(3)), int(m.group(4)) + 1)
            [clay.add((x, y)) for y in range(*ys)]
            min_y, max_y = min(min_y, int(m.group(3))), max(max_y, int(m.group(4)))
            min_x, max_x = min(min_x, x), max(max_x, x)
        else:
            xs, y = (int(m.group(3)), int(m.group(4)) + 1), int(m.group(2))
            [clay.add((x, y)) for x in range(*xs)]
            min_y, max_y = min(min_y, y), max(max_y, y)
            min_x, max_x = min(min_x, int(m.group(3))), max(max_x, int(m.group(4)))

    simulate()
    return len([w for w in water.values() if w.y >= min_y])


def day17b(puzzle_input: str) -> int:
    global water, min_y
    return len([w for w in water.values() if w.y >= min_y and w.settled])


if __name__ == '__main__':
    day17_input = get_input('day17.txt')
    print(day17a(day17_input))
    print(day17b(day17_input))
