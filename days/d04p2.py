from utils.parse import Parser
from itertools import tee


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def is_valid(password):
    group_len = 1
    is_adjacent_pair_same = False
    for first, second in pairwise(password):
        if first > second:
            return False

        if first == second:
            group_len += 1
        else:
            if group_len == 2:
                is_adjacent_pair_same = True
            group_len = 1

    # catch adjacency on last pair
    if group_len == 2:
        is_adjacent_pair_same = True

    return is_adjacent_pair_same


parser = Parser()
with parser.input as input:
    a, b = map(int, input.readline().split('-'))

n_valid = sum(is_valid(str(n)) for n in range(a, b+1))

print(n_valid)
