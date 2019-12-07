from utils.parse import Parser


class Grid:
    def __init__(self):
        self.__cells = set()

    def wire(self, direction, start, length):
        {
            'L': self.__left,
            'R': self.__right,
            'U': self.__up,
            'D': self.__down
        }[direction](start, length)

    @property
    def cells(self):
        return self.__cells

    def __up(self, start, length):
        x_s, y_s = start
        for y in range(y_s + 1, y_s + length + 1):
            cell = x_s, y
            self.__cells.add(cell)

    def __down(self, start, length):
        x_s, y_s = start
        for y in range(y_s - 1, y_s - length - 1, -1):
            cell = x_s, y
            self.__cells.add(cell)

    def __left(self, start, length):
        x_s, y_s = start
        for x in range(x_s - 1, x_s - length - 1, -1):
            cell = x, y_s
            self.__cells.add(cell)

    def __right(self, start, length):
        x_s, y_s = start
        for x in range(x_s + 1, x_s + length + 1):
            cell = x, y_s
            self.__cells.add(cell)


def move_pos(pos, d, l):
    x, y = pos

    if d == 'L':
        return x - l, y
    elif d == 'R':
        return x + l, y
    elif d == 'U':
        return x, y + l
    else:
        return x, y - l


def dist(pos):
    x, y = pos
    return abs(x) + abs(y)


parser = Parser("Day 3: Crossed Wires - Part 1")
with parser.input as input:
    line1 = input.readline()
    wire_a = [(path[:1], int(path[1:])) for path in line1.strip().split(',')]
    line2 = input.readline()
    wire_b = [(path[:1], int(path[1:])) for path in line2.strip().split(',')]

grid_a = Grid()
current_pos = (0, 0)
for d, l in wire_a:
    grid_a.wire(d, current_pos, l)
    current_pos = move_pos(current_pos, d, l)

grid_b = Grid()
current_pos = (0, 0)
for d, l in wire_b:
    grid_b.wire(d, current_pos, l)
    current_pos = move_pos(current_pos, d, l)

intersections = grid_a.cells & grid_b.cells
distances = map(dist, intersections)
closest_dist = min(distances)

print(closest_dist)
