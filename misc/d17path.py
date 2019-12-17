from utils.parse import Parser
from aoc.intcode import Machine
from copy import deepcopy
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
        new_value = (self._value_ + size + clockwise_turns) % size
        return Direction(new_value)


class Pixel(Enum):
    SPACE = (0, False)
    SCAFFOLD = (1, False)
    ROBOT_NORTH = (2, True)
    ROBOT_EAST = (3, True)
    ROBOT_SOUTH = (4, True)
    ROBOT_WEST = (5, True)

    def __new__(cls, value, is_robot):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.is_robot = is_robot
        return obj


class Camera:
    def __init__(self, program):
        self.__cpu = Machine(program, lambda: None, self.__get_pixel)
        self.__image = {}
        self.__position = (0, 0)
        self.__vacuum_robot = None

        self.__char_mapping = {
            '.': Pixel.SPACE,
            '#': Pixel.SCAFFOLD,
            '^': Pixel.ROBOT_NORTH,
            '>': Pixel.ROBOT_EAST,
            'v': Pixel.ROBOT_SOUTH,
            '<': Pixel.ROBOT_WEST
        }

        self.__dir_mapping = {
            Pixel.ROBOT_NORTH: Direction.NORTH,
            Pixel.ROBOT_EAST: Direction.EAST,
            Pixel.ROBOT_SOUTH: Direction.SOUTH,
            Pixel.ROBOT_WEST: Direction.WEST
        }

    @property
    def image(self):
        return self.__image

    @property
    def vacuum_robot(self):
        return self.__vacuum_robot

    def run(self):
        self.__cpu.run()

    def __get_pixel(self, ascii):
        c = chr(ascii)
        x, y = self.__position

        mapping = self.__char_mapping.get(c, None)
        if mapping is None:
            self.__position = 0, y + 1
            return

        if mapping.is_robot:
            robot_dir = self.__dir_mapping[mapping]
            self.__vacuum_robot = self.__position, self.__dir_mapping[mapping]

        self.__image[self.__position] = mapping
        self.__position = x + 1, y


parser = Parser("Day 17: Set and Forget - Path Finder")
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

turns = [(1, 'R'), (-1, 'L')]
path = []
steps_forward = 0
pos, dir = camera.vacuum_robot
while True:
    x, y = pos
    az_x, az_y = dir.azimuth
    position_forward = x + az_x, y + az_y

    if image.get(position_forward, None) is Pixel.SCAFFOLD:
        pos = position_forward
        steps_forward += 1
    else:
        dirs = ((dir.turn(n), instr) for n, instr in turns)
        turn_dirs = ((d, d.azimuth, instr) for d, instr in dirs)
        turn_positions = ((d, (x + a_x, y + a_y), instr) for d, (a_x, a_y), instr in turn_dirs)
        valid_positions = ((d, i) for d, p, i in turn_positions if image.get(p, None) is Pixel.SCAFFOLD)
        turned_direction, instruction = next(valid_positions, (None, None))

        if turned_direction is None:
            path.append(steps_forward)
            break

        dir = turned_direction
        if steps_forward > 0:
            path.append(steps_forward)
        path.append(instruction)
        steps_forward = 0

print(*path)
