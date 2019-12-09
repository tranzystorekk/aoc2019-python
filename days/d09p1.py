from utils.parse import Parser
from misc.intcode import Machine
from copy import deepcopy

parser = Parser("Day 9: Sensor Boost - Part 1")
with parser.input as input:
    line = input.readline()
    program = [int(el) for el in line.split(',')]

program_input = lambda: 1
computer = Machine(deepcopy(program), program_input)
computer.run()
