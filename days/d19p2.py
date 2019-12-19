from utils.parse import Parser
from aoc.intcode import Machine
from copy import deepcopy
from itertools import product


class Scanner:
    def __init__(self, program, grid_size):
        self.__program_copy = program
        self.__grid_size = grid_size
        self.__grid = {}
        self.__drone = None
        self.__next_position = None
        self.__next_position_it = None

    @property
    def grid(self):
        return self.__grid

    def run(self):
        for pos in product(range(self.__grid_size), range(self.__grid_size)):
            self.__next_position = pos
            self.__next_position_it = iter(self.__next_position)
            self.__drone = Machine(deepcopy(self.__program_copy), self.__get_position, self.__get_output)
            self.__drone.run()

    def __get_position(self):
        return next(self.__next_position_it)

    def __get_output(self, value):
        self.__grid[self.__next_position] = value


parser = Parser("Day 19: Tractor Beam - Part 1")
parser.parse()
with parser.input as input:
    line = input.readline()
    program = [int(el) for el in line.split(',')]

size = 100
scanner = Scanner(deepcopy(program), size)
scanner.run()

grid = scanner.grid

rows = [['#' if grid[(x, y)] == 1 else '.' for x in range(size)] for y in range(size)]
printed = ("".join(r) for r in rows)

print(*printed, sep='\n')
