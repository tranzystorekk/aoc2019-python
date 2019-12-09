from utils.parse import Parser
from misc.intcode import Machine
from itertools import product
from copy import deepcopy

parser = Parser("Day 2: 1202 Program Alarm - Part 2")
with parser.input as input:
    line = input.readline()
    program = [int(el) for el in line.split(',')]

for noun, verb in product(range(100), range(100)):
    program[1] = noun
    program[2] = verb
    computer = Machine(deepcopy(program), lambda: None)
    computer.run()
    output = computer.read(0)
    if output == 19690720:
        solution = 100 * noun + verb
        print(solution)
        break
