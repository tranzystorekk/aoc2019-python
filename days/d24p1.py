from utils.parse import Parser
from itertools import product, chain
from enum import Enum


class Entity(Enum):
    EMPTY = 0
    BUG = 1


class GameOfLife:
    __dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    __infestation_cond = [1, 2]

    def __init__(self, initial_state):
        self.__prev = initial_state
        self.__current = None

        elems = (self.__prev[pos] for pos in product(range(5), range(5)))
        initial_biodiv = sum(1 << i for i, el in enumerate(elems) if el is Entity.BUG)

        self.__recorded_states = {initial_biodiv}

    @property
    def current_biodiversity(self):
        coords = ((x, y) for y, x in product(range(5), range(5)))
        return sum(1 << i for i, pos in enumerate(coords) if self.__current[pos] is Entity.BUG)

    def run(self):
        while True:
            self.__step()

            current_elems = (self.__current[pos] for pos in product(range(5), range(5)))
            current_biodiv = sum(1 << i for i, el in enumerate(current_elems) if el is Entity.BUG)

            if current_biodiv in self.__recorded_states:
                break

            self.__recorded_states.add(current_biodiv)
            self.__prev = self.__current

    def __step(self):
        self.__current = {pos: self.__calculate_state(pos) for pos in product(range(5), range(5))}

    def __calculate_state(self, pos):
        x, y = pos
        adjacent = ((x + az_x, y + az_y) for az_x, az_y in GameOfLife.__dirs)
        n_adjacent_bugs = sum(1 for p in adjacent if self.__prev.get(p, Entity.EMPTY) is Entity.BUG)

        current_state = self.__prev[pos]

        if current_state is Entity.EMPTY and n_adjacent_bugs in GameOfLife.__infestation_cond:
            return Entity.BUG

        if current_state is Entity.BUG and n_adjacent_bugs != 1:
            return Entity.EMPTY

        return current_state


parser = Parser("Day 24: Planet of Discord - Part 1")
parser.parse()
with parser.input as input:
    coords = ((x, y) for y, x in product(range(5), range(5)))
    stripped = (l.strip() for l in input)
    chained = chain.from_iterable(stripped)
    mappings = {'.': Entity.EMPTY, '#': Entity.BUG}
    initial_state = {pos: mappings[v] for pos, v in zip(coords, chained)}

game = GameOfLife(initial_state)
game.run()

print(game.current_biodiversity)
