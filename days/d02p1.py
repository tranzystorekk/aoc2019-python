from utils.parse import Parser
from itertools import zip_longest
import operator


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


class Computer:
    def __init__(self, program):
        self.__memory = program

    def run(self):
        self.__running = True
        for opcode, a, b, dst in grouper(self.__memory, 4):
            self.__exec(opcode, a, b, dst)
            if not self.__running:
                break

    def set_1202(self):
        self.__memory[1] = 12
        self.__memory[2] = 2

    def read(self, pos):
        return self.__memory[pos]

    def __exec(self, opcode, a, b, dst):
        {
            1: self.__op(operator.add),
            2: self.__op(operator.mul),
            99: self.__terminate
        }[opcode](a, b, dst)

    def __terminate(self, a, b, dst):
        self.__running = False

    def __op(self, op):
        def ret_op(src_a, src_b, dst):
            a = self.__memory[src_a]
            b = self.__memory[src_b]
            result = op(a, b)
            self.__memory[dst] = result
        return ret_op


parser = Parser()
with parser.input as input:
    line = input.readline()
    program = [int(el) for el in line.split(',')]

computer = Computer(program.copy())
computer.set_1202()
computer.run()

zero_pos = computer.read(0)
print(zero_pos)
