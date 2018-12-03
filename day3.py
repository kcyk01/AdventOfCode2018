from utils import get_input
import re


def day3a(puzzle_input: str) -> int:
    matrix = [[0 for _ in range(1000)] for _ in range(1000)]
    for line in puzzle_input.strip().split('\n'):
        m = re.match(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', line)
        claim, row, col, w, h = int(m.group(1)), int(m.group(3)), int(m.group(2)), int(m.group(4)), int(m.group(5))
        for i in range(h):
            matrix[row + i][col:col + w] = [min(2, j + 1) for j in matrix[row + i][col:col + w]]
    return sum(map(lambda r: r.count(2), matrix))


def day3b(puzzle_input: str) -> int:
    matrix = [[0 for _ in range(1000)] for _ in range(1000)]
    overlapped_claims = set()
    all_claims = set()
    for line in puzzle_input.strip().split('\n'):
        m = re.match(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', line)
        claim, row, col, w, h = int(m.group(1)), int(m.group(3)), int(m.group(2)), int(m.group(4)), int(m.group(5))
        all_claims.add(claim)
        for i in range(h):
            for j in range(w):
                existing_claim = matrix[row + i][col + j]
                if existing_claim != 0:
                    overlapped_claims.add(existing_claim)
                    overlapped_claims.add(claim)
                matrix[row + i][col + j] = claim
    return list(all_claims.difference(overlapped_claims))[0]


if __name__ == '__main__':
    day3_input = get_input('day3.txt')
    print(day3a(day3_input))
    print(day3b(day3_input))
