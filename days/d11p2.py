from utils.parse import Parser
from aoc.intcode import Machine
from copy import deepcopy
from collections import defaultdict
from enum import Enum


class Direction(Enum):
    NORTH = (0, (0, 1))
    EAST = (1, (1, 0))
    SOUTH = (2, (0, -1))
    WEST = (3, (-1, 0))

    def __new__(cls, value, azimuth):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.azimuth = azimuth
        return obj

    def turn(self, side):
        size = len(self._member_names_)
        new_value = (self._value_ + size + side) % size
        return Direction(new_value)


class Painter:
    def __init__(self, program):
        self.__cpu = Machine(
            program, self.__get_panel_color, self.__get_instructions)
        self.__coordinates = 0, 0
        self.__dir = Direction.NORTH
        self.__grid = defaultdict(int)
        self.__current_color = 0
        self.__color__given = False

        self.__grid[(0, 0)] = 1

    @property
    def grid(self):
        return self.__grid

    def paint(self):
        self.__cpu.run()

    def __move(self):
        x_s, y_s = self.__dir.azimuth
        x, y = self.__coordinates
        self.__coordinates = x + x_s, y + y_s

    def __paint_panel(self):
        self.__grid[self.__coordinates] = self.__current_color

    def __get_panel_color(self):
        return self.__grid[self.__coordinates]

    def __get_instructions(self, value):
        if self.__color__given:
            turn_side = 1 if value else -1
            self.__dir = self.__dir.turn(turn_side)
            self.__move()
            self.__color__given = False
        else:
            self.__current_color = value
            self.__paint_panel()
            self.__color__given = True


parser = Parser("Day 11: Space Police - Part 2")
parser.parse()
with parser.input as input:
    line = input.readline()
    program = [int(el) for el in line.strip().split(',')]

painter = Painter(deepcopy(program))
painter.paint()

white_panels = {coords for coords, color in painter.grid.items() if color == 1}
max_x = max(x for x, _ in white_panels)
max_y = max(y for _, y in white_panels)
min_x = min(x for x, _ in white_panels)
min_y = min(y for _, y in white_panels)

painted_grid = [['#' if (x, y) in white_panels else ' ' for x in range(
    min_x, max_x + 1)] for y in range(max_y, min_y - 1, -1)]
rows = ("".join(r) for r in painted_grid)
print(*rows, sep='\n')
