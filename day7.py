import re

from utils import get_input

worker_count = 5
nodes = {}
starting_queue = []

worker_queue = []
node_queue = []


def day7a(puzzle_input: str) -> str:
    global nodes, starting_queue
    for line in puzzle_input.strip().split('\n'):
        m = re.match(r'.*Step (\w+) .* step (\w+) can begin', line)
        first, second = m.group(1), m.group(2)
        if first not in nodes:
            nodes[first] = Node(first)
        if second not in nodes:
            nodes[second] = Node(second)
        nodes[first].add_dependent(nodes[second])
        nodes[second].add_requirement(nodes[first])

    starting_queue = []
    for name, node in nodes.items():
        if len(node.requires) == 0:
            starting_queue.append(name)

    queue = starting_queue[:]
    order = ''
    while len(queue) > 0:
        queue = list(set(queue))
        queue.sort()

        name = queue.pop(0)
        order += name
        node = nodes[name]

        completed = set(order)
        for dependent in node.dependents:
            if len({n.name for n in dependent.requires}.difference(completed)) == 0:
                queue.append(dependent.name)
    return order


class Node:
    def __init__(self, name: str):
        self.name = name
        self.requires = []
        self.dependents = []

    def __repr__(self):
        return self.name

    def add_requirement(self, r):
        self.requires.append(r)

    def add_dependent(self, d):
        self.dependents.append(d)


class Worker:
    completed = ''
    letters = '.ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    def __init__(self, name: int):
        self.name = name
        self.time = 0
        self.node = None

    def assign_work(self, node):
        self.node = node
        self.time = Worker.letters.find(node.name) + 60

    def tick(self):
        global worker_queue, node_queue
        self.time -= 1
        if self.time == 0:
            worker_queue.append(self)
            Worker.completed += self.node.name
            for dependent in self.node.dependents:
                if len({n.name for n in dependent.requires}.difference(Worker.completed)) == 0:
                    node_queue.append(dependent.name)


def day7b(puzzle_input: str) -> int:
    global worker_count, worker_queue, node_queue, starting_queue
    workers = [Worker(i) for i in range(worker_count)]
    worker_queue = workers[:]
    node_queue = starting_queue[:]
    time = 0
    while len(node_queue) > 0 or len(worker_queue) != worker_count:
        node_queue.sort()
        if len(worker_queue) == 0 or len(node_queue) == 0:
            time += 1
            for worker in workers:
                worker.tick()
        else:
            worker = worker_queue.pop(0)
            name = node_queue.pop(0)
            worker.assign_work(nodes[name])
    return time


if __name__ == '__main__':
    day7_input = get_input('day7.txt')
    print(day7a(day7_input))
    print(day7b(day7_input))
