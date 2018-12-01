from utils import get_input


def day1a(puzzle_input: str) -> int:
    return sum([int(num) for num in puzzle_input.strip().split('\n')])


def day1b(puzzle_input: str) -> int:
    nums = [int(num) for num in puzzle_input.strip().split('\n')]
    freq_set = set()
    freq = i = 0
    while True:
        freq += int(nums[i])
        if freq in freq_set:
            return freq
        freq_set.add(freq)
        i = (i + 1) % len(nums)


if __name__ == '__main__':
    day1_input = get_input('day1.txt')
    print(day1a(day1_input))
    print(day1b(day1_input))
