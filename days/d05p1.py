from utils.parse import Parser
import operator


def reverse_digits(n):
    current = n
    while True:
        yield current % 10
        current //= 10


class Computer:
    def __init__(self, program):
        self.__memory = program
        self.__output = 0

    @property
    def last_output(self):
        return self.__output

    def run(self, input_func):
        self.__running = True
        self.__pc = 0
        self.__in_f = input_func
        while True:
            opcode, args = self.__parse_instruction()
            self.__exec(opcode, args)
            if not self.__running:
                break
            self.__pc += len(args) + 1

    def read(self, pos):
        return self.__memory[pos]

    def write(self, pos, value):
        self.__memory[pos] = value

    def __exec(self, opcode, args):
        {
            1: self.__op(operator.add),
            2: self.__op(operator.mul),
            3: self.__in,
            4: self.__out,
            99: self.__terminate
        }[opcode](args)

    def __parse_instruction(self):
        opcode = self.__memory[self.__pc]
        op = opcode % 100
        names = []
        if op == 1 or op == 2:
            names = ['a', 'b', 'dst']
        elif op == 3 or op == 4:
            names = ['addr']

        return op, self.__get__args(names, opcode // 100)

    def __get__args(self, names, mode_code):
        modes = reverse_digits(mode_code)
        return {name: (mode, self.__memory[self.__pc + pos]) for pos, (name, mode) in enumerate(zip(names, modes), 1)}

    def __terminate(self, args):
        self.__running = False

    def __op(self, op):
        def ret_op(args):
            m_a, v_a = args['a']
            a = self.__get_from_mode(m_a, v_a)
            m_b, v_b = args['b']
            b = self.__get_from_mode(m_b, v_b)
            result = op(a, b)
            _, dst = args['dst']
            self.__memory[dst] = result
        return ret_op

    def __in(self, args):
        _, addr = args['addr']
        self.__memory[addr] = self.__in_f()

    def __out(self, args):
        m, v = args['addr']
        self.__output = self.__get_from_mode(m, v)

    def __get_from_mode(self, mode, v):
        if mode == 1:
            return v

        return self.__memory[v]


parser = Parser()
with parser.input as input:
    line = input.readline()
    program = [int(el) for el in line.split(',')]

program_input = lambda: 1
computer = Computer(program)
computer.run(program_input)

print(computer.last_output)
