from utils.parse import Parser
from _collections import deque
from itertools import compress, chain
from enum import Enum


class Direction(Enum):
    NORTH = (0, (0, -1))
    EAST = (1, (1, 0))
    SOUTH = (2, (0, 1))
    WEST = (3, (-1, 0))

    def __new__(cls, value, azimuth):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.azimuth = azimuth
        return obj

    def turn(self, clockwise_turns):
        size = len(Direction)
        new_value = (self._value_ + clockwise_turns + size) % size
        return Direction(new_value)


def get_grid_from_lines(lines):
    width = len(lines[0])
    flat = [c for line in lines for c in line]
    grid = {(i % width, i // width): c if c.isupper() else '.' for i, c in enumerate(flat) if c != '#'}
    keys = {(i % width, i // width): c for i, c in enumerate(flat) if c.islower()}
    start_pos = next((i % width, i // width) for i, c in enumerate(flat) if c == '@')

    return start_pos, keys, grid


def find_keys(grid, keys, pos, current_keys):
    current_searchspace = deque([(0, pos)])
    visited = set()
    gathered_keys = []
    while current_searchspace:
        # print(current_searchspace)
        distance, current_pos = current_searchspace.popleft()
        x, y = current_pos
        if current_pos in keys:
            gathered_keys.append((distance, current_pos, keys[current_pos]))

        # print(current_pos)
        visited.add(current_pos)

        azims = (d.azimuth for d in Direction)
        choices = ((x + az_x, y + az_y) for az_x, az_y in azims)
        valid_choices = [choice for choice in choices if choice in grid and choice not in visited]
        rooms = (grid[c] for c in valid_choices)
        # print("Adjacent rooms:", rooms)
        doors = (not r.isupper() or r.lower() in current_keys for r in rooms)
        valid_paths = ((distance + 1, path) for path in compress(valid_choices, doors))
        # print("Valid paths:", valid_paths)

        current_searchspace.extend(valid_paths)

    return gathered_keys


parser = Parser()
parser.parse()
with parser.input as input:
    lines = [l.strip() for l in input]

print(*lines, sep='\n')

start, keys, grid = get_grid_from_lines(lines)

initial_keys = find_keys(grid, keys, start, set())
key_searchspace = deque((set(), dist, kpos, key) for dist, kpos, key in initial_keys)
distances = []
while(key_searchspace):
    prev_keys, d, kpos, k = key_searchspace.popleft()

    currently_owned_keys = set(k for k in chain(prev_keys, [k]))
    remaining_keys = {p: k for p, k in keys.items() if k not in currently_owned_keys}
    remaining_set = set(k for k in remaining_keys.values())

    print("Owned:", currently_owned_keys)
    print("Remaining:", remaining_keys)

    newfound_keys = find_keys(grid, remaining_keys, kpos, currently_owned_keys)
    nf_set = set(k for _, _, k in newfound_keys)
    if not remaining_set - nf_set:
        distances.append(d)

    key_searchspace.extend((currently_owned_keys, d, kp, k) for d, kp, k in newfound_keys)

print(distances)
