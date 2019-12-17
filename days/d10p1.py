from utils.parse import Parser
from math import gcd
from itertools import chain, takewhile, dropwhile, product


def scanline(x, y, w_step, h_step):
    current_x, current_y = x, y
    while True:
        current_x += w_step
        current_y += h_step
        yield current_x, current_y


def normalize(p):
    a, b = p
    divisor = gcd(a, b)
    return a // divisor, b // divisor


def count_visible_from(x, y, w, h, asteroids):
    angles = {normalize(p) for p in product(range(1, w), range(1, h))}
    signs = [1, -1]
    all_signs = ((w_s * sign_w, h_s * sign_h) for (w_s, h_s), sign_w, sign_h in product(angles, signs, signs))
    straight_lines = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    lines = chain(all_signs, straight_lines)

    n_visible = 0
    for w_s, h_s in lines:
        sline = takewhile(lambda p: w > p[0] >= 0 and h > p[1] >= 0, scanline(x, y, w_s, h_s))
        dropped = dropwhile(lambda p: p not in asteroids, sline)
        n_visible += 1 if any(True for _ in dropped) else 0

    return n_visible


parser = Parser("Day 10: Monitoring Station - Part 1")
parser.parse()
with parser.input as input:
    data = [line.strip() for line in input]

width = len(data[0])
height = len(data)

flattened = "".join(data)
asteroids = {(i % width, i // width) for i, symbol in enumerate(flattened) if symbol == '#'}

max_visible = max(count_visible_from(x, y, width, height, asteroids) for x, y in asteroids)
print(max_visible)
