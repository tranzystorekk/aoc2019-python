from utils.parse import Parser
from copy import deepcopy
from itertools import permutations, tee, cycle, islice
import operator


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


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
    def __init__(self, program, inp_func, out_func):
        self.__memory = program
        self.__in_f = inp_func
        self.__out_f = out_func
        self.__output = 0
        self.__halted = False
        self.__pc = 0
        self.__jump_flag = False
        self.__jump_addr = 0

    @property
    def last_output(self):
        return self.__output

    @property
    def halted(self):
        return self.__halted

    def run(self):
        self.__running = True
        while True:
            opcode, args = self.__parse_instruction()
            self.__exec(opcode, args)
            if self.__jump_flag:
                self.__pc = self.__jump_addr
                self.__jump_flag = False
            else:
                self.__pc += len(args) + 1
            if not self.__running:
                break

    def start_or_resume(self):
        if not self.__halted:
            self.run()

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
        self.__halted = True

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
        out_v = self.__get_from_mode(m, v)
        self.__output = out_v
        self.__out_f(out_v)
        self.__running = False

    def __get_from_mode(self, mode, v):
        if mode == 1:
            return v

        return self.__memory[v]


class Link:
    def __init__(self, phase, init_value):
        self.__phase = phase
        self.__value = init_value
        self.__phase_given = False

    def __call__(self, v=None):
        if not v:
            return self.__get_value()

        self.__value = v

    def __get_value(self):
        if self.__phase_given:
            return self.__value

        self.__phase_given = True
        return self.__phase


def run_feedback_loop(phases, prog):
    links = [Link(p, 0) for p in phases]
    linkage = pairwise(cycle(links))
    comps = [Computer(deepcopy(prog), i, o) for i, o in islice(linkage, len(links))]
    while not all(c.halted for c in comps):
        for c in comps:
            c.start_or_resume()

    return comps[-1].last_output


parser = Parser("Day 7: Amplification Circuit - Part 2")
with parser.input as input:
    line = input.readline()
    program = [int(el) for el in line.split(',')]

max_output = max(run_feedback_loop(t, program) for t in permutations(range(5, 10)))

print(max_output)
