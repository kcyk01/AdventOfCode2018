from utils import get_input

grid_size = 300
matrix = {}
sat = {}


def get_power(grid_serial: int, x: int, y: int) -> int:
    rack_id = x + 10
    return (y * rack_id + grid_serial) * rack_id // 100 % 10 - 5


def find_max_convolution(n: int) -> tuple:
    global grid_size
    max_power, location = -100000, None
    for i in range(grid_size - n + 1):
        for j in range(grid_size - n + 1):
            power = (sat[i + n - 1, j + n - 1] -
                     (0 if i - 1 < 0 else sat[i - 1, j + n - 1]) -
                     (0 if j - 1 < 0 else sat[i + n - 1, j - 1]) +
                     (0 if i - 1 < 0 or j - 1 < 0 else sat[i - 1, j - 1]))
            if power > max_power:
                max_power, location = power, (j + 1, i + 1)
    return max_power, location


def day11a(puzzle_input: str) -> str:
    global grid_size, matrix
    grid_serial = int(puzzle_input.strip())
    for i in range(grid_size):
        for j in range(grid_size):
            matrix[i, j] = get_power(grid_serial, j + 1, i + 1)
            sat[i, j] = ((0 if i - 1 < 0 else sat[i - 1, j]) +
                         (0 if j - 1 < 0 else sat[i, j - 1]) -
                         (0 if i - 1 < 0 or j - 1 < 0 else sat[i - 1, j - 1]) +
                         matrix[i, j])

    _, location = find_max_convolution(3)
    return '{},{}'.format(location[0], location[1])


def day11b(puzzle_input: str) -> str:
    global grid_size
    size, max_power, max_location = -1, -100000, None
    for i in range(2, grid_size):
        power, location = find_max_convolution(i)
        if power > max_power:
            size, max_power, max_location = i, power, location
    return '{},{},{}'.format(max_location[0], max_location[1], size)


if __name__ == '__main__':
    day11_input = get_input('day11.txt')
    print(day11a(day11_input))
    print(day11b(day11_input))
