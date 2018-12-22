from utils import get_input

points = {}
direction = {
    'E': lambda x, y: (x + 1, y),
    'W': lambda x, y: (x - 1, y),
    'N': lambda x, y: (x, y - 1),
    'S': lambda x, y: (x, y + 1)
}
stack = []


class Point:
    def __init__(self, x: int, y: int, path: list):
        self.x = x
        self.y = y
        self.path = path
        self.dist = len(self.path)
        self.adjacent = []

    def __repr__(self):
        return '({},{})'.format(self.x, self.y)

    def add_adjacent(self, point):
        self.adjacent.append(point)


def day20a(puzzle_input: str) -> int:
    global stack, points, direction
    start = (0, 0)
    p = Point(start[0], start[1], [])
    points[start] = p
    for c in puzzle_input:
        if c == '^' or c == '$':
            continue
        if c == ')':
            stack.pop()
        elif c == '|':
            p = stack[-1]
        elif c == '(':
            stack.append(p)
        else:
            next_pos = direction[c](p.x, p.y)
            p.add_adjacent(next_pos)
            new_point = Point(next_pos[0], next_pos[1], p.path + [(p.x, p.y)])
            new_point.add_adjacent((p.x, p.y))
            if next_pos not in points:
                points[next_pos] = new_point
            else:
                # Point already visited, only store the shorter distance
                existing = points[next_pos]
                if existing.dist > new_point.dist:
                    points[next_pos] = new_point
            p = new_point

    farthest = max(points.items(), key=lambda kv: kv[1].dist)[0]
    return points[farthest].dist


def day20b(puzzle_input: str) -> int:
    global points
    return len([1 for point in points.values() if point.dist >= 1000])


if __name__ == '__main__':
    day20_input = get_input('day20.txt')
    print(day20a(day20_input))
    print(day20b(day20_input))
