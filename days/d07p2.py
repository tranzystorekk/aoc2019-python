from utils.parse import Parser
from aoc.intcode import Machine
from copy import deepcopy
from itertools import permutations, tee, cycle, islice


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


class Link:
    def __init__(self, phase, init_value):
        self.__phase = phase
        self.__value = init_value
        self.__phase_given = False

    def __call__(self, v=None):
        if v is None:
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
    comps = [Machine(deepcopy(prog), i, o) for i, o in islice(linkage, len(links))]
    for c in comps:
        c.break_on_output = True
    while not all(c.halted for c in comps):
        for c in comps:
            c.start_or_resume()

    return comps[-1].last_output


parser = Parser("Day 7: Amplification Circuit - Part 2")
parser.parse()
with parser.input as input:
    line = input.readline()
    program = [int(el) for el in line.split(',')]

max_output = max(run_feedback_loop(t, program) for t in permutations(range(5, 10)))

print(max_output)
