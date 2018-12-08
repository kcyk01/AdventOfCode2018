from utils import get_input

nodes = {}


def day8a(puzzle_input: str) -> int:
    global nodes
    node_stack = []
    nums = puzzle_input.strip().split()
    i, node_id = 0, 0
    c_size = -1
    while i < len(nums) and len(node_stack) >= 0:
        num = nums[i]
        if len(node_stack) > 0 and node_stack[0].has_all_children():
            # Extract metadata
            n = node_stack.pop(0)
            j = i + n.metadata_count
            n.set_metadata([int(x) for x in nums[i:j]])
            i = j
        elif c_size == -1:
            # Set the first part of the header
            c_size = int(num)
            i += 1
        else:
            # Get second part of header, create the node and add to stack
            md_size = int(num)
            nodes[node_id] = Node(c_size, md_size)
            if len(node_stack) > 0:
                # Attach to parent if applicable
                n = node_stack[0]
                n.add_child(nodes[node_id])
            node_stack.insert(0, nodes[node_id])
            node_id += 1
            i += 1
            c_size = -1
    return sum([sum(n.metadata) for n in nodes.values()])


class Node:
    def __init__(self, c_size: int, md_size: int):
        self.children = []
        self.metadata = []
        self.children_count = c_size
        self.metadata_count = md_size
        self.value = 0

    def has_all_children(self):
        return self.children_count == len(self.children)

    def add_child(self, child):
        self.children.append(child)

    def set_metadata(self, metadata: list):
        self.metadata = metadata
        if self.children_count == 0:
            self.value = sum(metadata)
        else:
            self.value = sum([self.children[md - 1].value for md in metadata if md <= self.children_count])


def day8b(puzzle_input: str) -> int:
    return nodes[0].value


if __name__ == '__main__':
    day8_input = get_input('day8.txt')
    print(day8a(day8_input))
    print(day8b(day8_input))
