from utils import get_input


def day2a(puzzle_input: str) -> int:
    m, n = 0, 0
    for line in puzzle_input.strip().split('\n'):
        two, three = 0, 0
        for char in set(line):
            if line.count(char) == 2:
                two = 1
            if line.count(char) == 3:
                three = 1
        m += two
        n += three
    return m * n


def day2b(puzzle_input: str) -> str:
    patterns = set()
    for line in puzzle_input.strip().split('\n'):
        for i in range(len(line)):
            pattern = line[:i] + '.' + line[i+1:]
            if pattern in patterns:
                return pattern.replace('.', '')
            patterns.add(pattern)


if __name__ == '__main__':
    day2_input = get_input('day2.txt')
    print(day2a(day2_input))
    print(day2b(day2_input))
