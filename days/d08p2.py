from utils.parse import Parser
from itertools import zip_longest, dropwhile


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def get_color(pixel_stack):
    skip_transparent = dropwhile(lambda p: p == '2', pixel_stack)
    return next(skip_transparent)


def printable_color(c):
    return '#' if c == '1' else ' '


parser = Parser("Day 8: Space Image Format - Part 2")
with parser.input as input:
    data = input.readline().strip()

w = 25
h = 6
layer_size = w * h
layers = grouper(data, layer_size)

decoded = [get_color(p) for p in zip(*layers)]
rows = ("".join(map(printable_color, r)) for r in grouper(decoded, w))

print(*rows, sep='\n')
