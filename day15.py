import re

from utils import get_input
from collections import defaultdict

terrain = []


class Monster:
    monsters = {}

    def __init__(self, x: int, y: int, dmg: int = 3):
        self.x = x
        self.y = y
        self.hp = 200
        self.dmg = dmg
        self.possible_moves = []
        self.near_enemies = []

    def _can_attack(self, enemy_type) -> bool:
        self.near_enemies = Monster.find_adjacent_enemies(self.x, self.y, enemy_type)
        return len(self.near_enemies) > 0

    def _can_move(self, enemy_type) -> bool:
        self.possible_moves = []
        if self._can_attack(enemy_type):
            return False
        self.possible_moves = Monster.find_adjacent_spaces(self.x, self.y)
        return len(self.possible_moves) > 0

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp <= 0:
            # Remove instance from simulation
            if (self.x, self.y) in Goblin.goblins:
                del Goblin.goblins[self.x, self.y]
            elif (self.x, self.y) in Elf.elves:
                del Elf.elves[self.x, self.y]
            Monster.update()

    def attack(self) -> bool:
        if len(self.near_enemies) == 0:
            return False

        enemy = sorted(self.near_enemies, key=lambda e: (e.hp, e.y, e.x))[0]
        enemy.take_damage(self.dmg)

        return True

    def _move(self, enemies: dict, allies: dict) -> bool:
        # Find all points one away from the enemy
        targets = set()
        for elf in enemies.values():
            targets = targets.union(set(Monster.find_adjacent_spaces(elf.x, elf.y)))

        next_move = Monster.get_next_move((self.x, self.y), targets)
        if next_move is None:
            # No possible next move
            return False

        # Update position
        del allies[self.x, self.y]
        self.x, self.y = next_move
        allies[next_move] = self
        Monster.update()

        return True

    @staticmethod
    def update():
        Monster.monsters = {**Elf.elves, **Goblin.goblins}

    @staticmethod
    def get_next_move(start: tuple, targets: set):
        if len(targets) == 0:
            # No target can be reached
            return None

        distances = Monster.calculate_distances(start, targets)
        if len(distances) == 0:
            # No possible paths to any target
            return None

        closest_target = sorted(distances.keys(), key=lambda pt: (pt[1], pt[0]))[0]
        return sorted(set([pair[0] for pair in distances[closest_target]]), key=lambda pt: (pt[1], pt[0]))[0]

    @staticmethod
    def find_adjacent_spaces(x: int, y: int) -> list:
        global terrain
        up, down, left, right = (x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)
        possible_moves = []
        if terrain[up[1]][up[0]] != '#' and up not in Monster.monsters:
            possible_moves.append(up)
        if terrain[left[1]][left[0]] != '#' and left not in Monster.monsters:
            possible_moves.append(left)
        if terrain[right[1]][right[0]] != '#' and right not in Monster.monsters:
            possible_moves.append(right)
        if terrain[down[1]][down[0]] != '#' and down not in Monster.monsters:
            possible_moves.append(down)
        return possible_moves

    @staticmethod
    def find_adjacent_enemies(x: int, y: int, enemy_type) -> list:
        up, down, left, right = (x, y - 1), (x, y + 1), (x - 1, y), (x + 1, y)
        enemies = []
        if up in Monster.monsters and type(Monster.monsters[up]) == enemy_type:
            enemies.append(Monster.monsters[up])
        if left in Monster.monsters and type(Monster.monsters[left]) == enemy_type:
            enemies.append(Monster.monsters[left])
        if right in Monster.monsters and type(Monster.monsters[right]) == enemy_type:
            enemies.append(Monster.monsters[right])
        if down in Monster.monsters and type(Monster.monsters[down]) == enemy_type:
            enemies.append(Monster.monsters[down])
        return enemies

    @staticmethod
    def calculate_distances(start: tuple, ends: set) -> dict:
        global terrain
        distances = defaultdict(list)
        queue, queue_points = [(start, None, 0)], {start}
        while len(ends.difference(distances.keys())) > 0 and len(queue) > 0:
            point, first, length = queue.pop(0)
            queue_points.remove(point)

            # Check if a closest path to a end point has already been found
            diff = list(ends.difference(ends.difference(distances.keys())))
            if len(diff) > 0 and distances[diff[0]][0][1] < length:
                # All closest paths of the same distance found (paths in the queue are all longer)
                break

            if terrain[point[1]][point[0]] != '.' or length != 0 and point in Monster.monsters:
                # Ignore points that are not walkable
                continue

            # Save the first point of this path and the length of this path
            first = point if first is None and length != 0 else first
            distances[point].append((first, length))

            # Add adjacent points of this new point to the queue
            adjacent = Monster.find_adjacent_spaces(point[0], point[1])
            for adj_point in adjacent:
                # Only add if the point has not already been visited or not already in the queue
                if adj_point not in distances and adj_point not in queue_points:
                    queue.append((adj_point, first, length + 1))
                    queue_points.add(adj_point)
        return {k: v for k, v in distances.items() if k in ends}


class Elf(Monster):
    elves = {}

    def __init__(self, x: int, y: int, dmg: int = 3):
        super().__init__(x, y, dmg)

    def can_attack(self) -> bool:
        return Monster._can_attack(self, Goblin)

    def can_move(self) -> bool:
        return Monster._can_move(self, Goblin)

    def move(self) -> bool:
        return Monster._move(self, Goblin.goblins, Elf.elves)


class Goblin(Monster):
    goblins = {}

    def __init__(self, x: int, y: int):
        super().__init__(x, y, 3)

    def can_attack(self) -> bool:
        return Monster._can_attack(self, Elf)

    def can_move(self) -> bool:
        return Monster._can_move(self, Elf)

    def move(self) -> bool:
        return Monster._move(self, Elf.elves, Goblin.goblins)


def init(puzzle_input: str, elf_dmg: int = 3):
    global terrain
    Elf.elves, Goblin.goblins, terrain = {}, {}, []
    for i, line in enumerate(puzzle_input.strip().split('\n')):
        for match in re.finditer(r'[EG]', line):
            x, y = match.start(), i
            if match.group() == 'E':
                Elf.elves[x, y] = Elf(x, y, elf_dmg)
            else:
                Goblin.goblins[x, y] = Goblin(x, y)
        terrain.append(list(re.sub(r'[EG]', '.', line)))
    Monster.update()


def simulate() -> str:
    rounds = 0
    while True:
        monsters = sorted(Monster.monsters.items(), key=lambda kv: (kv[0][1], kv[0][0]))
        i, cannot_move = 0, 0
        for i, (pos, monster) in enumerate(monsters):
            if pos not in Monster.monsters:
                # Already dead, skip
                continue

            if monster.can_attack():
                # Attack if can attack right away
                monster.attack()
            elif monster.can_move() and monster.move():
                # Cannot attack, try to move, then attack
                monster.can_attack() and monster.attack()
            else:
                # Cannot move or attack
                cannot_move += 1

            if len(Elf.elves) == 0 or len(Goblin.goblins) == 0:
                # Combat ended
                break

        if len(monsters) == cannot_move or len(Elf.elves) == 0 or len(Goblin.goblins) == 0:
            # Combat ended or stalemate, if full round completed, add full round count
            rounds += 1 if i == len(monsters) - 1 else 0
            break
        rounds += 1
    return sum([monster.hp for monster in Monster.monsters.values()]) * rounds


def day15a(puzzle_input: str) -> str:
    init(puzzle_input, 3)
    return simulate()


def day15b(puzzle_input: str) -> str:
    dmg = 4
    while True:
        init(puzzle_input, dmg)
        starting_elves = len(Elf.elves)
        score = simulate()
        if starting_elves == len(Elf.elves):
            return score
        dmg += 1


if __name__ == '__main__':
    day15_input = get_input('day15.txt')
    print(day15a(day15_input))
    print(day15b(day15_input))
