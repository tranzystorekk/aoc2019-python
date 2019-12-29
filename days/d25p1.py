from utils.parse import Parser
from aoc.intcode import Machine
from itertools import chain


class Droid:
    def __init__(self, program):
        self.__cpu = Machine(program, self.__get_input, self.__get_output)
        self.__input = None
        self.__input_it = iter(())
        self.__output = []

    def run(self):
        self.__cpu.run()

        if self.__output:
            self.__flush_output()

    def __get_input(self):
        if self.__output:
            self.__flush_output()

        c = next(self.__input_it, None)

        if c is None:
            input_line = input('#> ')
            self.__input = [input_line, '\n']
            self.__input_it = chain.from_iterable(self.__input)
            c = next(self.__input_it)

        return ord(c)

    def __get_output(self, ascii):
        c = chr(ascii)
        self.__output.append(c)

    def __flush_output(self):
        outprint = "".join(self.__output)
        print(outprint)
        self.__output.clear()


# This part is interactive, navigate Santa's ship and get through the Pressure-Sensitive Floor to win!
parser = Parser("Day 25: Cryostasis - Part 1")
parser.parse()
with parser.input as inp:
    line = inp.readline()
    program = [int(el) for el in line.split(',')]

droid = Droid(program)
droid.run()
