from utils.parse import Parser
from aoc.intcode import Machine
from copy import deepcopy

parser = Parser("Day 2: 1202 Program Alarm - Part 1")
with parser.input as input:
    line = input.readline()
    program = [int(el) for el in line.split(',')]

program[1] = 12
program[2] = 2
computer = Machine(deepcopy(program), lambda: None)
computer.run()

zero_pos = computer.read(0)
print(zero_pos)
