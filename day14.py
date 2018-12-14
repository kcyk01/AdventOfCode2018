from utils import get_input


def update_recipes(scores: list, pos1: int, pos2: int) -> tuple:
    s = scores[pos1] + scores[pos2]
    if s >= 10:
        scores.append(s // 10)
    scores.append(s % 10)
    return (pos1 + scores[pos1] + 1) % len(scores), (pos2 + scores[pos2] + 1) % len(scores)


def day14a(puzzle_input: str) -> str:
    target = int(puzzle_input)
    scores, pos1, pos2 = [3, 7], 0, 1
    while len(scores) < target + 10:
        pos1, pos2 = update_recipes(scores, pos1, pos2)
    return ''.join([str(scores[target + i]) for i in range(10)])


def day14b(puzzle_input: str) -> int:
    recipe_size = len(puzzle_input)
    scores, pos1, pos2 = [3, 7], 0, 1
    window = '37'
    while True:
        prev_len = len(scores)
        pos1, pos2 = update_recipes(scores, pos1, pos2)
        diff = len(scores) - prev_len
        window += (str(scores[-2]) if diff > 1 else '') + str(scores[-1])
        if puzzle_input in window:
            return len(scores) - recipe_size - 1
        window = window[-recipe_size:]


if __name__ == '__main__':
    day14_input = get_input('day14.txt')
    print(day14a(day14_input))
    print(day14b(day14_input))
