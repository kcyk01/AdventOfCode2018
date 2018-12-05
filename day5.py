import re

from utils import get_input

lower = 'abcdefghijklmnopqrstuvwxyz'
upper = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def day5a(puzzle_input: str) -> int:
    text = puzzle_input
    pairs = [a + b for a, b in zip(lower, upper)] + [a + b for a, b in zip(upper, lower)]
    letter_map = {s[0]: s[1] for s in pairs}
    pattern = '|'.join(pairs)

    text, n = re.subn(pattern, '', text)
    while n > 0:
        text, n = re.subn(pattern, '', text)
        m = re.search(pattern, text)

        if m is None:
            break

        # Find mirroring matching pairs going outwards and remove it all at once to reduce the amount of outer loops
        for i in range(len(text)):
            start, end = m.start() - i, m.end() + i
            if start < 0 or end >= len(text) or letter_map[text[start]] != text[end - 1]:
                text = text[:start + 1] + text[end - 1:]
                break
    return len(text)


def day5b(puzzle_input: str) -> int:
    letters = [a + b for a, b in zip(lower, upper)]
    lowest = len(puzzle_input)
    for removal in letters:
        new_length = day5a(puzzle_input.replace(removal[0], '').replace(removal[1], ''))
        if new_length < lowest:
            lowest = new_length
    return lowest


if __name__ == '__main__':
    day5_input = get_input('day5.txt')
    print(day5a(day5_input))
    print(day5b(day5_input))
