import re

size = 10
offset = 0
matrix = [[None for _ in range(size)] for _ in range(size)]

names = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
queue = []


def day6_sim(puzzle_input: str):
    global size, offset, matrix, names, queue

    for i, line in enumerate(puzzle_input.strip().split('\n')):
        m = re.match(r'(\d+), (\d+)', line)
        p = Point(names[i], int(m.group(1)) + offset, int(m.group(2)) + offset)
        matrix[p.y][p.x] = p
        queue.append(p)

    while len(queue) > 0:
        p = queue.pop(0)
        p.step()
        print_matrix()
        print('\n')


def print_matrix():
    for row in matrix:
        print(''.join([str(point) if point is not None else ' ' for point in row]))


class Point:
    global size, matrix, queue

    def __init__(self, name: str, x: int, y: int, dist: int = 0):
        self.name = name
        self.x = x
        self.y = y
        self.dist = dist

    def __str__(self):
        return self.name

    def step(self):
        left, right, up, down = self.x - 1, self.x + 1, self.y - 1, self.y + 1
        if left >= 0:
            Point.update(matrix[self.y][left], Point(self.name, left, self.y, self.dist + 1))
        if right < size:
            Point.update(matrix[self.y][right], Point(self.name, right, self.y, self.dist + 1))
        if up >= 0:
            Point.update(matrix[up][self.x], Point(self.name, self.x, up, self.dist + 1))
        if down < size:
            Point.update(matrix[down][self.x], Point(self.name, self.x, down, self.dist + 1))

    @staticmethod
    def update(prev_point, new_point):
        if prev_point is None or new_point.dist < prev_point.dist:
            matrix[new_point.y][new_point.x] = new_point
            queue.append(new_point)
        elif prev_point.dist == new_point.dist and prev_point.name != new_point.name:
            prev_point.name = '.'


if __name__ == '__main__':
    day6_input = '''1, 1
1, 6
8, 3
3, 4
5, 5
8, 9'''
    print(day6_sim(day6_input))
