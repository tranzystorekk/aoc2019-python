from utils.parse import Parser
from aoc.intcode import Machine
from itertools import product
from copy import deepcopy


def run_with_params(program, noun, verb):
    program[1] = noun
    program[2] = verb
    computer = Machine(deepcopy(program), lambda: None)
    computer.run()
    return computer.read(0)


parser = Parser("Day 2: 1202 Program Alarm - Part 2")
parser.parse()
with parser.input as input:
    line = input.readline()
    program = [int(el) for el in line.split(',')]

filtered = ((n, v) for n, v in product(range(100), range(100)) if run_with_params(program, n, v) == 19690720)
noun, verb = next(filtered)

solution = 100 * noun + verb
print(solution)
