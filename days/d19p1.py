from utils.parse import Parser
from aoc.intcode import Machine
from copy import deepcopy
from itertools import product


class Scanner:
    def __init__(self, program, grid_size):
        self.__program_copy = program
        self.__grid_size = grid_size
        self.__drone = None
        self.__pulled = 0
        self.__next_position = None

    @property
    def pulled(self):
        return self.__pulled

    def run(self):
        for pos in product(range(self.__grid_size), range(self.__grid_size)):
            self.__next_position = iter(pos)
            self.__drone = Machine(
                deepcopy(self.__program_copy), self.__get_position, self.__get_output)
            self.__drone.run()

    def __get_position(self):
        return next(self.__next_position)

    def __get_output(self, value):
        self.__pulled += value


parser = Parser("Day 19: Tractor Beam - Part 1")
parser.parse()
with parser.input as input:
    line = input.readline()
    program = [int(el) for el in line.split(',')]

scanner = Scanner(deepcopy(program), 50)
scanner.run()

print(scanner.pulled)
