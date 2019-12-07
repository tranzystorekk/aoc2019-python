from utils.parse import Parser


class Grid:
    def __init__(self):
        self.__cells = {}
        self.__steps = 0

    def wire(self, direction, start, length):
        {
            'L': self.__left,
            'R': self.__right,
            'U': self.__up,
            'D': self.__down
        }[direction](start, length)

    @property
    def intersections(self):
        return self.__intersections

    @property
    def cells(self):
        return self.__cells

    @property
    def cell_set(self):
        return set(self.__cells.keys())

    def __up(self, start, length):
        x_s, y_s = start
        for y in range(y_s + 1, y_s + length + 1):
            self.__steps += 1
            cell = x_s, y
            if not cell in self.__cells:
                self.__cells[cell] = self.__steps

    def __down(self, start, length):
        x_s, y_s = start
        for y in range(y_s - 1, y_s - length - 1, -1):
            self.__steps += 1
            cell = x_s, y
            if not cell in self.__cells:
                self.__cells[cell] = self.__steps

    def __left(self, start, length):
        x_s, y_s = start
        for x in range(x_s - 1, x_s - length - 1, -1):
            self.__steps += 1
            cell = x, y_s
            if not cell in self.__cells:
                self.__cells[cell] = self.__steps

    def __right(self, start, length):
        x_s, y_s = start
        for x in range(x_s + 1, x_s + length + 1):
            self.__steps += 1
            cell = x, y_s
            if not cell in self.__cells:
                self.__cells[cell] = self.__steps


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


parser = Parser("Day 3: Crossed Wires - Part 2")
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

cells_a = grid_a.cell_set
cells_b = grid_b.cell_set
intersections = cells_a & cells_b

steps = (grid_a.cells[cell] + grid_b.cells[cell] for cell in intersections)
closest = min(steps)

print(closest)
