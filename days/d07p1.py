from utils.parse import Parser
from misc.intcode import Machine
from copy import deepcopy
from itertools import permutations


class Input:
    def __init__(self, phase, input_value):
        seq = [phase, input_value]
        self.__it = iter(seq)

    def __call__(self):
        return next(self.__it)


def run_series(phases, prog):
    value = 0
    program_output = lambda v: None
    for p in phases:
        program_input = Input(p, value)
        computer = Machine(deepcopy(prog), program_input, program_output)
        computer.run()
        value = computer.last_output
    return value


parser = Parser("Day 7: Amplification Circuit - Part 1")
with parser.input as input:
    line = input.readline()
    program = [int(el) for el in line.split(',')]

max_output = max(run_series(t, program) for t in permutations(range(5)))

print(max_output)
