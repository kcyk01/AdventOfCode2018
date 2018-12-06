import re

from utils import get_input
from collections import defaultdict


size = 500
offset = size / 4
names = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
points = {}


def day6a(puzzle_input: str) -> int:
    global size, offset, names, points
    matrix = [['' for _ in range(size)] for _ in range(size)]
    for i, line in enumerate(puzzle_input.strip().split('\n')):
        m = re.match(r'(\d+), (\d+)', line)
        points[names[i]] = (int(m.group(1)) + offset, int(m.group(2)) + offset)

    for i in range(size):
        for j in range(size):
            matrix[i][j] = find_closest(i, j)

    counts = defaultdict(int)
    excluded = (set(matrix[0])
                .union(set(matrix[-1]))
                .union({row[0] for row in matrix})
                .union({row[-1] for row in matrix})
                .union({'.'}))
    for row in matrix:
        for name in set(row).difference(excluded):
            counts[name] += row.count(name)
    return max(counts.items(), key=lambda kv: kv[1])[1]


def find_closest(i: int, j: int) -> str:
    global points
    lowest, minimum = '.', size
    for name, point in points.items():
        dist = abs(point[0] - j) + abs(point[1] - i)
        if dist == minimum:
            lowest = '.'
        if dist < minimum:
            lowest, minimum = name, dist
    return lowest


def day6b(puzzle_input: str) -> int:
    global size, points
    matrix = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = sum_distances(i, j)
    return sum([sum(row) for row in matrix])


def sum_distances(i: int, j: int) -> int:
    global points
    s = 0
    for name, point in points.items():
        s += abs(point[0] - j) + abs(point[1] - i)
    return 1 if s < 10000 else 0


if __name__ == '__main__':
    day6_input = get_input('day6.txt')
    print(day6a(day6_input))
    print(day6b(day6_input))
