from utils.parse import Parser
from copy import deepcopy
from itertools import permutations
import operator


def reverse_digits(n):
    current = n
    while True:
        yield current % 10
        current //= 10


class Args:
    def __init__(self, args):
        self.__dict__.update(args)

    def __len__(self):
        return len(self.__dict__)


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
        self.__jump_flag = False
        self.__jump_addr = 0
        while True:
            opcode, args = self.__parse_instruction()
            self.__exec(opcode, args)
            if not self.__running:
                break
            if self.__jump_flag:
                self.__pc = self.__jump_addr
                self.__jump_flag = False
            else:
                self.__pc += len(args) + 1

    def read(self, pos):
        return self.__memory[pos]

    def write(self, pos, value):
        self.__memory[pos] = value

    def __exec(self, opcode, args):
        {
            1: self.__arithmetic_op(operator.add),
            2: self.__arithmetic_op(operator.mul),
            3: self.__in,
            4: self.__out,
            5: self.__jump_op(lambda v: v != 0),
            6: self.__jump_op(lambda v: v == 0),
            7: self.__comp_op(operator.lt),
            8: self.__comp_op(operator.eq),
            99: self.__terminate
        }[opcode](args)

    def __parse_instruction(self):
        opcode = self.__memory[self.__pc]
        op = opcode % 100
        names = []
        if op == 1 or op == 2 or op == 7 or op == 8:
            names = ['a', 'b', 'dst']
        elif op == 5 or op == 6:
            names = ['cond', 'addr']
        elif op == 3 or op == 4:
            names = ['addr']

        return op, self.__get__args(names, opcode // 100)

    def __get__args(self, names, mode_code):
        modes = reverse_digits(mode_code)
        arg_begin = self.__pc + 1
        args = {name: (mode, value) for name, mode, value in zip(names, modes, self.__memory[arg_begin:])}
        return Args(args)

    def __terminate(self, args):
        self.__running = False

    def __arithmetic_op(self, op):
        def ret_op(args):
            m_a, v_a = args.a
            a = self.__get_from_mode(m_a, v_a)
            m_b, v_b = args.b
            b = self.__get_from_mode(m_b, v_b)
            result = op(a, b)
            _, dst = args.dst
            self.__memory[dst] = result
        return ret_op

    def __comp_op(self, op):
        def ret_op(args):
            m_a, v_a = args.a
            a = self.__get_from_mode(m_a, v_a)
            m_b, v_b = args.b
            b = self.__get_from_mode(m_b, v_b)
            _, dst = args.dst
            self.__memory[dst] = 1 if op(a, b) else 0
        return ret_op

    def __jump_op(self, pred):
        def ret_op(args):
            m_cond, v_cond = args.cond
            cond = self.__get_from_mode(m_cond, v_cond)
            m_addr, v_addr = args.addr
            self.__jump_addr = self.__get_from_mode(m_addr, v_addr)
            self.__jump_flag = pred(cond)
        return ret_op

    def __in(self, args):
        _, addr = args.addr
        self.__memory[addr] = self.__in_f()

    def __out(self, args):
        m, v = args.addr
        self.__output = self.__get_from_mode(m, v)

    def __get_from_mode(self, mode, v):
        if mode == 1:
            return v

        return self.__memory[v]


class Input:
    def __init__(self, phase, input_value):
        seq = [phase, input_value]
        self.__it = iter(seq)

    def __call__(self):
        return next(self.__it)


def run_series(phases, prog):
    value = 0
    for p in phases:
        computer = Computer(deepcopy(prog))
        inp = Input(p, value)
        computer.run(inp)
        value = computer.last_output
    return value


parser = Parser()
with parser.input as input:
    line = input.readline()
    program = [int(el) for el in line.split(',')]

max_output = max(run_series(t, program) for t in permutations(range(5)))

print(max_output)
