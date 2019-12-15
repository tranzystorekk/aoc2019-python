from utils.parse import Parser
from aoc.intcode import Machine
from copy import deepcopy
from enum import Enum


class Room(Enum):
    WALL = 0
    FREE = 1
    OXYGEN = 2


class Direction(Enum):
    NORTH = (0, (0, 1), 1)
    EAST = (1, (1, 0), 4)
    SOUTH = (2, (0, -1), 2)
    WEST = (3, (-1, 0), 3)

    def __new__(cls, value, azimuth, instruction):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.azimuth = azimuth
        obj.instruction = instruction
        return obj

    def turn(self, cwise_turns):
        size = len(Direction)
        new_value = (self._value_ + size + cwise_turns) % size
        return Direction(new_value)


class Controller:
    __turns = [1, -1, -1, -1]

    def __init__(self, program):
        self.__droid = Machine(program, self.__get_direction, self.__get_status)
        self.__droid.break_on_output = True
        self.__position = (0, 0)
        self.__direction = Direction.EAST
        self.__room_map = {(0, 0): Room.FREE}
        self.__decision_picker = iter(Controller.__turns)
        self.__oxygen_system_found = False

    @property
    def position(self):
        return self.__position

    @property
    def room_map(self):
        return self.__room_map

    def run(self):
        while not self.__oxygen_system_found:
            self.__droid.start_or_resume()

    def __get_direction(self):
        return self.__direction.instruction

    def __get_status(self, status):
        room = Room(status)

        x, y = self.__position
        az_x, az_y = self.__direction.azimuth
        new_pos = x + az_x, y + az_y

        self.__room_map[new_pos] = room

        if room is not Room.WALL:
            self.__position = new_pos
            self.__decision_picker = iter(Controller.__turns)

        if room is Room.OXYGEN:
            self.__oxygen_system_found = True

        decision = next(self.__decision_picker)
        self.__direction = self.__direction.turn(decision)


def get_printable_field(x, y, pos, map):
    print_mappings = {Room.FREE: '.', Room.WALL: '#', Room.OXYGEN: 'X'}
    p = x, y
    if p == pos:
        return 'D'

    if p == (0, 0):
        return 'S'

    room = map.get(p, None)
    return print_mappings.get(room, ' ')


def print_map(pos, map):
    max_x = max(x for x, _ in map.keys())
    max_y = max(y for _, y in map.keys())
    min_x = min(x for x, _ in map.keys())
    min_y = min(y for _, y in map.keys())

    map = [[get_printable_field(x, y, pos, map) for x in range(min_x, max_x + 1)] for y in range(max_y, min_y - 1, -1)]

    rows = ("".join(r) for r in map)
    print(*rows, sep='\n')
    print()


def shortest_path(ship_map):
    current_searchspace = [(0, (0, 0))]
    visited = set()
    while current_searchspace:
        path_length, p = current_searchspace.pop()

        current_room = ship_map.get(p, None)
        if current_room is Room.OXYGEN:
            return path_length

        visited.add(p)
        directions = (d.azimuth for d in Direction)

        x, y = p
        choices = [(x + a_x, y + a_y) for a_x, a_y in directions]
        mapped = map(lambda p: ship_map.get(p, None), choices)
        choices_mapped = ((c, m) for c, m in zip(choices, mapped) if m is not None)
        selected_paths = ((path_length + 1, choice) for choice, room in choices_mapped if choice not in visited and room is not Room.WALL)
        current_searchspace.extend(selected_paths)

    return None


parser = Parser()
with parser.input as input:
    line = input.readline()
    program = [int(el) for el in line.split(',')]


controller = Controller(deepcopy(program))
controller.run()

solution = shortest_path(controller.room_map)

print(solution)
