import re

from utils import get_input

duration = 0


class Point:
    lowest_x = 100000
    lowest_y = 100000
    highest_x = -100000
    highest_y = -100000

    def __init__(self, pos: tuple, vel: tuple):
        self.position = pos
        self.velocity = vel
        Point.update(self.position[0], self.position[1])

    def tick(self, reverse=False):
        if reverse:
            self.position = (self.position[0] - self.velocity[0], self.position[1] - self.velocity[1])
        else:
            self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])
        Point.update(self.position[0], self.position[1])

    @staticmethod
    def reset():
        Point.lowest_x = 100000
        Point.lowest_y = 100000
        Point.highest_x = -100000
        Point.highest_y = -100000

    @staticmethod
    def update(x, y):
        if x <= Point.lowest_x:
            Point.lowest_x = x
        if y <= Point.lowest_y:
            Point.lowest_y = y
        if x >= Point.highest_x:
            Point.highest_x = x
        if y >= Point.highest_y:
            Point.highest_y = y

    @staticmethod
    def get_range_spread():
        return abs(Point.highest_y - Point.lowest_y) * abs(Point.highest_x - Point.lowest_x)


def day10a(puzzle_input: str) -> None:
    global duration
    points = []
    for line in puzzle_input.strip().split('\n'):
        nums = re.findall(r'(-?\d+)', line)
        points.append(Point((int(nums[0]), int(nums[1])), (int(nums[2]), int(nums[3]))))

    spread = Point.get_range_spread()
    while True:
        Point.reset()
        [point.tick() for point in points]
        if Point.get_range_spread() > spread:
            break
        spread = Point.get_range_spread()
        duration += 1

    Point.reset()
    [point.tick(reverse=True) for point in points]
    print_matrix(points)


def print_matrix(points):
    matrix = [['.' for _ in range(Point.highest_x - Point.lowest_x + 1)] for _ in range(Point.highest_y - Point.lowest_y + 1)]
    for point in points:
        matrix[point.position[1] - Point.lowest_y][point.position[0] - Point.lowest_x] = '#'
    for row in matrix:
        print(''.join(row))


def day10b(puzzle_input: str) -> int:
    global duration
    return duration


if __name__ == '__main__':
    day10_input = get_input('day10.txt')
    day10a(day10_input)
    print(day10b(day10_input))
