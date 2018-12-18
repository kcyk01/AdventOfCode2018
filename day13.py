import re

from utils import get_input

carts_by_positions = {}
tracks = []
collisions = []


class Cart:
    dir_map = {
        '<': 0,
        '^': 1,
        '>': 2,
        'v': 3
    }

    '''
    Numerical representation of left, straight, and right moves that occur at intersections
    
    This along with dir_map above allows easy directional change by subtracting 1 for left turns, or adding 1 for right
    turns (with modulo 4 to normalize back to the 4 directions)
    '''
    intersection_moves = [-1, 0, 1]

    '''
    Maps the tuple (track, current direction) to a callable function that returns the next direction
        - Corners just redirect in the 90-degree turn direction
        - Straight lines just return the same direction
        - Intersection accounts for the last intersection move (function arg)
    '''
    move_map = {
        ('/', 0): lambda _: 3,
        ('/', 1): lambda _: 2,
        ('/', 2): lambda _: 1,
        ('/', 3): lambda _: 0,
        ('\\', 0): lambda _: 1,
        ('\\', 1): lambda _: 0,
        ('\\', 2): lambda _: 3,
        ('\\', 3): lambda _: 2,
        ('-', 0): lambda _: 0,
        ('-', 2): lambda _: 2,
        ('|', 1): lambda _: 1,
        ('|', 3): lambda _: 3,
        ('+', 0): lambda n: n % 4,
        ('+', 1): lambda n: (1 + n) % 4,
        ('+', 2): lambda n: (2 + n) % 4,
        ('+', 3): lambda n: (3 + n) % 4
    }

    def __init__(self, cart_id: int, x: int, y: int, direction: int):
        self.id = cart_id
        self.x = x
        self.y = y
        self.direction = direction
        self.next_intersection = 0

    def __repr__(self):
        return str(self.id)

    def move(self) -> tuple:
        global tracks
        if self.direction == 0:
            self.x -= 1
        elif self.direction == 1:
            self.y -= 1
        elif self.direction == 2:
            self.x += 1
        else:
            self.y += 1

        new_track = tracks[self.y][self.x]
        self.direction = Cart.move_map[new_track, self.direction](Cart.intersection_moves[self.next_intersection])
        if new_track == '+':
            self.next_intersection = (self.next_intersection + 1) % 3
        return self.x, self.y


def day13a(puzzle_input: str) -> str:
    global tracks, collisions, carts_by_positions
    for i, line in enumerate(puzzle_input.rstrip().split('\n')):
        tracks.append(re.sub(r'[\^v]', '|', re.sub(r'[<>]', '-', line)))
        for match in re.finditer(r'[<>^v]', line):
            x, y = match.start(), i
            carts_by_positions[x, y] = Cart(len(carts_by_positions), x, y, Cart.dir_map[match.group()])

    while len(carts_by_positions) > 1:
        # Carts sorted top to down, with left to right tie-break
        ordered_carts = sorted(carts_by_positions.items(), key=lambda kv: (kv[1].y, kv[1].x))

        for pos, cart in ordered_carts:
            if pos not in carts_by_positions:
                # Cart already collided and was removed
                continue

            del carts_by_positions[pos]
            new_pos = cart.move()
            if new_pos in carts_by_positions:
                # Collision detected
                other_cart = carts_by_positions[new_pos]
                collisions.append((new_pos, cart, other_cart))
                del carts_by_positions[new_pos]
            else:
                carts_by_positions[new_pos] = cart

    collision_position, _, _ = collisions[0]
    return '{},{}'.format(collision_position[0], collision_position[1])


def day13b(puzzle_input: str) -> str:
    global carts_by_positions
    last_cart_position = list(carts_by_positions.keys())[0]
    return '{},{}'.format(last_cart_position[0], last_cart_position[1])


def debug():
    global tracks
    temp_tracks = [list(t) for t in tracks]
    for pos, cart in carts_by_positions.items():
        temp_tracks[pos[1]][pos[0]] = '<^>v'[cart.direction]
    for row in temp_tracks:
        print(''.join(row))
    print()


if __name__ == '__main__':
    day13_input = get_input('day13.txt')
    print(day13a(day13_input))
    print(day13b(day13_input))
