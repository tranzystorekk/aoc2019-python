from utils.parse import Parser
from itertools import islice


def reverse_digits(n):
    current = n
    while True:
        yield current % 10
        current //= 10


def reverse_digits_bound(n):
    current = n
    while current > 0:
        yield current % 10
        current //= 10


def get_n_args(op):
    n = 0
    if op == 1 or op == 2 or op == 7 or op == 8:
        n = 3
    elif op == 5 or op == 6:
        n = 2
    elif op == 3 or op == 4:
        n = 1

    return n


def is_valid(opcode):
    op = opcode % 100
    if op not in {1, 2, 3, 4, 5, 6, 7, 8, 99}:
        return False

    mode_codes = list(reverse_digits_bound(opcode // 100))
    if any(m not in {0, 1} for m in mode_codes):
        return False

    n_mode_codes = len(mode_codes)
    n_expected = get_n_args(op)
    return n_mode_codes <= n_expected


def get_args(arg_slice, n_args, mode_code):
    modes = reverse_digits(mode_code)
    return [(mode, value) for mode, value in islice(zip(modes, arg_slice), n_args)]


def parse_instruction(prog_slice):
    opcode = prog_slice[0]
    if not is_valid(opcode):
        return None, []

    op = opcode % 100
    n = get_n_args(op)

    return op, get_args(prog_slice[1:], n, opcode // 100)


def get_arg_symbol(code):
    return "#" if code == 1 else ""


parser = Parser("Intcode prettifier")
with parser.input as input:
    line = input.readline()
    program = [int(el) for el in line.split(',')]

names = {1: "ADD", 2: "MUL", 3: "INP", 4: "OUT", 5: "JNZ", 6: "JEZ", 7: "TLT", 8: "TEQ", 99: "HLT"}

pos = 0
size = len(program)
while pos < size:
    current_slice = program[pos:]
    op, args = parse_instruction(current_slice)

    name = names.get(op, "??? ({})".format(program[pos]))
    formatted_args = ("{}{}".format(get_arg_symbol(code), value) for code, value in args)
    pos_marker = "{:08}:".format(pos)
    print(pos_marker, name, *formatted_args)

    pos += len(args) + 1
