from utils.parse import Parser
from aoc.intcode import Machine
from copy import deepcopy
from enum import Enum


class Tile(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4

    def __new__(cls, value):
        obj = object.__new__(cls)
        obj._value_ = value
        return obj


class PaintState(Enum):
    NOTHING_READ = 0
    X_READ = 1
    Y_READ = 2

    def __new__(cls, value):
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def advance(self):
        value = self._value_
        value = (value + 1) % len(self._member_names_)
        return PaintState(value)


class Arcade:
    def __init__(self, program):
        self.__cpu = Machine(program, self.__get_joystick, self.__get_instructions)
        self.__grid = {}
        self.__paint_state = PaintState.NOTHING_READ
        self.__score = 0
        self.__x = None
        self.__y = None

        self.__ball_current_position = None
        self.__pad_position = None

        self.__state_actions = {
            PaintState.NOTHING_READ: self.__read_x,
            PaintState.X_READ: self.__read_y,
            PaintState.Y_READ: self.__paint_tile
        }

    @property
    def grid(self):
        return self.__grid

    @property
    def score(self):
        return self.__score

    def run(self):
        self.__cpu.run()

    def __get_joystick(self):
        if self.__pad_position < self.__ball_current_position:
            return 1

        if self.__pad_position > self.__ball_current_position:
            return -1

        return 0

    def __get_instructions(self, value):
        self.__state_actions[self.__paint_state](value)
        self.__paint_state = self.__paint_state.advance()

    def __read_x(self, x):
        self.__x = x

    def __read_y(self, y):
        self.__y = y

    def __paint_tile(self, value):
        coords = self.__x, self.__y
        if coords == (-1, 0):
            self.__score = value
            return

        tile = Tile(value)
        self.__grid[coords] = tile

        if tile is Tile.BALL:
            self.__ball_current_position = self.__x
        elif tile is Tile.PADDLE:
            self.__pad_position = self.__x


parser = Parser("Day 13: Care Package - Part 2")
parser.parse()
with parser.input as input:
    line = input.readline()
    program = [int(el) for el in line.split(',')]

program[0] = 2
arcade = Arcade(deepcopy(program))
arcade.run()

print(arcade.score)
