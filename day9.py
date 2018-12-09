import re

from utils import get_input
from collections import defaultdict


class Node:
    def __init__(self, value: int, first_node: bool = False):
        self.prev = self if first_node else None
        self.next = self if first_node else None
        self.value = value

    def set_next(self, next_node):
        self.next = next_node

    def set_prev(self, prev_node):
        self.prev = prev_node

    def insert_after(self, inserted_node):
        next_node = self.next
        self.set_next(inserted_node)
        inserted_node.set_prev(self)
        inserted_node.set_next(next_node)
        next_node.set_prev(inserted_node)

    def pop(self) -> int:
        prev_node = self.prev
        next_node = self.next
        prev_node.set_next(next_node)
        next_node.set_prev(prev_node)
        return self.value


def day9a(puzzle_input: str) -> int:
    scores = defaultdict(int)
    current_node = Node(0, first_node=True)

    m = re.match(r'(\d+).*?(\d+)', puzzle_input.strip())
    players, last_marble = int(m.group(1)), int(m.group(2))
    for i in range(1, last_marble):
        if i % 23 == 0:
            scores[i % players] += i
            for _ in range(6):
                current_node = current_node.prev
            scores[i % players] += current_node.prev.pop()
        else:
            current_node.next.insert_after(Node(i))
            current_node = current_node.next.next
    return max(scores.items(), key=lambda kv: kv[1])[1]


def day9b(puzzle_input: str) -> int:
    return day9a(puzzle_input.replace(' points', '00 points'))


if __name__ == '__main__':
    day9_input = get_input('day9.txt')
    print(day9a(day9_input))
    print(day9b(day9_input))
