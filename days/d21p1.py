from utils.parse import Parser
from aoc.intcode import Machine


class SpringDroid:
    def __init__(self, program, springscript):
        self.__cpu = Machine(program, self.__get_input, lambda v: None)
        self.__script = springscript
        self.__it = iter(self.__script)

    @property
    def output(self):
        return self.__cpu.last_output

    def run(self):
        self.__cpu.run()

    def __get_input(self):
        c = next(self.__it)
        return ord(c)


parser = Parser("Day 21: Springdroid Adventure - Part 1")
parser.parse()
with parser.input as input:
    line = input.readline()
    program = [int(el) for el in line.split(',')]

script = (
    "NOT C J\n"
    "AND D J\n"
    "NOT A T\n"
    "OR T J\n"
    "WALK\n"
)

droid = SpringDroid(program, script)
droid.run()

print(droid.output)
