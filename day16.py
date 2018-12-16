import re

from utils import get_input
from collections import defaultdict


class Code:
    ops = {
        'addr': lambda args: Code.addr(*args),
        'addi': lambda args: Code.addi(*args),
        'mulr': lambda args: Code.mulr(*args),
        'muli': lambda args: Code.muli(*args),
        'banr': lambda args: Code.banr(*args),
        'bani': lambda args: Code.bani(*args),
        'borr': lambda args: Code.borr(*args),
        'bori': lambda args: Code.bori(*args),
        'setr': lambda args: Code.setr(*args),
        'seti': lambda args: Code.seti(*args),
        'gtir': lambda args: Code.gtir(*args),
        'gtri': lambda args: Code.gtri(*args),
        'gtrr': lambda args: Code.gtrr(*args),
        'eqir': lambda args: Code.eqir(*args),
        'eqri': lambda args: Code.eqri(*args),
        'eqrr': lambda args: Code.eqrr(*args),
    }
    number_to_possible = defaultdict(set)
    number_to_op = defaultdict(str)

    @staticmethod
    def addr(regs: list, in_reg_a: int, in_reg_b: int, out_reg: int):
        regs[out_reg] = regs[in_reg_a] + regs[in_reg_b]

    @staticmethod
    def addi(regs: list, in_reg_a: int, in_val_b: int, out_reg: int):
        regs[out_reg] = regs[in_reg_a] + in_val_b

    @staticmethod
    def mulr(regs: list, in_reg_a: int, in_reg_b: int, out_reg: int):
        regs[out_reg] = regs[in_reg_a] * regs[in_reg_b]

    @staticmethod
    def muli(regs: list, in_reg_a: int, in_val_b: int, out_reg: int):
        regs[out_reg] = regs[in_reg_a] * in_val_b

    @staticmethod
    def banr(regs: list, in_reg_a: int, in_reg_b: int, out_reg: int):
        regs[out_reg] = regs[in_reg_a] & regs[in_reg_b]

    @staticmethod
    def bani(regs: list, in_reg_a: int, in_val_b: int, out_reg: int):
        regs[out_reg] = regs[in_reg_a] & in_val_b

    @staticmethod
    def borr(regs: list, in_reg_a: int, in_reg_b: int, out_reg: int):
        regs[out_reg] = regs[in_reg_a] | regs[in_reg_b]

    @staticmethod
    def bori(regs: list, in_reg_a: int, in_val_b: int, out_reg: int):
        regs[out_reg] = regs[in_reg_a] | in_val_b

    @staticmethod
    def setr(regs: list, in_reg: int, _: int, out_reg: int):
        regs[out_reg] = regs[in_reg]

    @staticmethod
    def seti(regs: list, in_val: int, _: int, out_reg: int):
        regs[out_reg] = in_val

    @staticmethod
    def gtir(regs: list, in_val_a: int, in_reg_b: int, out_reg: int):
        regs[out_reg] = 1 if in_val_a > regs[in_reg_b] else 0

    @staticmethod
    def gtri(regs: list, in_reg_a: int, in_val_b: int, out_reg: int):
        regs[out_reg] = 1 if regs[in_reg_a] > in_val_b else 0

    @staticmethod
    def gtrr(regs: list, in_reg_a: int, in_reg_b: int, out_reg: int):
        regs[out_reg] = 1 if regs[in_reg_a] > regs[in_reg_b] else 0

    @staticmethod
    def eqir(regs: list, in_val_a: int, in_reg_b: int, out_reg: int):
        regs[out_reg] = 1 if in_val_a == regs[in_reg_b] else 0

    @staticmethod
    def eqri(regs: list, in_reg_a: int, in_val_b: int, out_reg: int):
        regs[out_reg] = 1 if regs[in_reg_a] == in_val_b else 0

    @staticmethod
    def eqrr(regs: list, in_reg_a: int, in_reg_b: int, out_reg: int):
        regs[out_reg] = 1 if regs[in_reg_a] == regs[in_reg_b] else 0


def day16a(puzzle_input: str) -> int:
    Code.number_to_possible = {i: set(Code.ops.keys()) for i in range(16)}
    first_half = puzzle_input.split('\n\n\n')[0]
    count = 0
    for section in first_half.split('\n\n'):
        m = [int(n) for n in re.findall(r'(\d+)', section, re.MULTILINE)]
        possible = set()

        # Try all the ops
        for opname, op in Code.ops.items():
            regs = m[:4]
            op((regs, *m[5:8]))
            if regs == m[8:]:
                possible.add(opname)

        # Update possible choices for that number
        Code.number_to_possible[m[4]] = Code.number_to_possible[m[4]].intersection(possible)

        if len(possible) >= 3:
            count += 1
    return count


def day16b(puzzle_input: str) -> int:
    # Identify the op numbers
    while len(Code.number_to_op) != 16:
        for num, possible in Code.number_to_possible.items():
            remaining = possible.difference(set(Code.number_to_op.values()))
            if len(remaining) == 1:
                Code.number_to_op[num] = list(remaining)[0]
            else:
                Code.number_to_possible[num] = remaining

    # Run the test input
    second_half = puzzle_input.split('\n\n\n')[1]
    regs = [0, 0, 0, 0]
    for command in second_half.strip().split('\n'):
        nums = [int(n) for n in command.split()]
        Code.ops[Code.number_to_op[nums[0]]]((regs, *nums[1:]))

    return regs[0]


if __name__ == '__main__':
    day16_input = get_input('day16.txt')
    print(day16a(day16_input))
    print(day16b(day16_input))
