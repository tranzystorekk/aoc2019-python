from utils.parse import Parser
from itertools import zip_longest, tee


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


parser = Parser("Day 8: Space Image Format - Part 1")
with parser.input as input:
    data = [int(c) for c in input.readline().strip()]

w, h = 25, 6
layer_size = w * h
layers = grouper(data, layer_size)
fewest_zeroes = min(layers, key=lambda l: sum(p == 0 for p in l))

ones = sum(p == 1 for p in fewest_zeroes)
twos = sum(p == 2 for p in fewest_zeroes)

print(ones * twos)
