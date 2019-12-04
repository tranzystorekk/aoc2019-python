from utils.parse import Parser
from itertools import tee


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def is_valid(password):
    is_adjacent_same = False
    for first, second in pairwise(password):
        if first == second:
            is_adjacent_same = True
        elif first > second:
            return False

    return is_adjacent_same


parser = Parser()
with parser.input as input:
    a, b = map(int, input.readline().split('-'))

n_valid = sum(is_valid(str(n)) for n in range(a, b+1))

print(n_valid)
