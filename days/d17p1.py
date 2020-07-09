from utils.parse import Parser
from aoc.intcode import Machine
from copy import deepcopy
from enum import Enum


class Pixel(Enum):
    SPACE = 0
    SCAFFOLD = 1


class Camera:
    def __init__(self, program):
        self.__cpu = Machine(program, lambda: None, self.__get_pixel)
        self.__image = {}
        self.__position = (0, 0)

        self.__char_mapping = {
            '.': Pixel.SPACE,
            '#': Pixel.SCAFFOLD,
            '^': Pixel.SCAFFOLD,
            '>': Pixel.SCAFFOLD,
            'v': Pixel.SCAFFOLD,
            '<': Pixel.SCAFFOLD
        }

    @property
    def image(self):
        return self.__image

    def run(self):
        self.__cpu.run()

    def __get_pixel(self, ascii):
        c = chr(ascii)
        x, y = self.__position

        mapping = self.__char_mapping.get(c, None)
        if mapping is None:
            self.__position = 0, y + 1
            return

        self.__image[self.__position] = mapping
        self.__position = x + 1, y


parser = Parser("Day 17: Set and Forget - Part 1")
parser.parse()
with parser.input as input:
    line = input.readline()
    program = [int(el) for el in line.split(',')]

camera = Camera(deepcopy(program))
camera.run()

image = camera.image

min_x = min(x for x, _ in image.keys())
min_y = min(y for _, y in image.keys())
max_x = max(x for x, _ in image.keys())
max_y = max(y for _, y in image.keys())

directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

scaffold_scan = ((x, y) for y in range(min_y, max_y + 1)
                 for x in range(min_x, max_x + 1) if image[(x, y)] is Pixel.SCAFFOLD)
total_alignment = 0
for x, y in scaffold_scan:
    adjacent = ((x + d_x, y + d_y) for d_x, d_y in directions)
    adjacent_scaffolds = sum(
        1 for p in adjacent if image.get(p, None) is Pixel.SCAFFOLD)
    if adjacent_scaffolds > 2:
        total_alignment += x * y

print(total_alignment)
