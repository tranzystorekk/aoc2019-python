from utils.parse import Parser
from math import gcd
from itertools import chain, takewhile, dropwhile, product, islice


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


def pseudoangle(point):
    x, y = point
    p = y / (abs(x) + abs(y))
    if x < 0:
        p = 2 - p

    return p


def generate_scans(w, h):
    angles = {normalize(p) for p in product(range(1, w), range(1, h))}
    signs = [1, -1]
    all_signs = ((w_s * sign_w, h_s * sign_h)
                 for (w_s, h_s), sign_w, sign_h in product(angles, signs, signs))
    return all_signs


def count_visible_from(x, y, w, h, asteroids):
    scans = generate_scans(w, h)
    straight_lines = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    lines = chain(scans, straight_lines)

    n_visible = 0
    for w_s, h_s in lines:
        sline = takewhile(
            lambda p: w > p[0] >= 0 and h > p[1] >= 0, scanline(x, y, w_s, h_s))
        dropped = dropwhile(lambda p: p not in asteroids, sline)
        n_visible += 1 if any(True for _ in dropped) else 0

    return n_visible


def clockwise_scanned(x, y, w, h, asteroids):
    scans = generate_scans(w, h)
    straight_lines = [(0, -1), (1, 0), (-1, 0)]
    lines = chain(scans, straight_lines)
    angle_sorted = sorted(lines, key=lambda p: pseudoangle(
        (-p[0], -p[1])), reverse=True)
    angle_sorted = chain([(0, 1)], angle_sorted)

    result = []
    for w_s, h_s in angle_sorted:
        # ugly hack to correct the discrepancy
        # between coordinates and the "up" direction
        h_s = -h_s

        sline = takewhile(
            lambda p: w > p[0] >= 0 and h > p[1] >= 0, scanline(x, y, w_s, h_s))
        scanned = [p for p in sline if p in asteroids]
        if scanned:
            result.append(scanned)

    return result


parser = Parser("Day 10: Monitoring Station - Part 2")
parser.parse()
with parser.input as input:
    data = [line.strip() for line in input]

width = len(data[0])
height = len(data)

flattened = "".join(data)
asteroids = {(i % width, i // width)
             for i, symbol in enumerate(flattened) if symbol == '#'}

x_max, y_max = max(asteroids, key=lambda p: count_visible_from(
    p[0], p[1], width, height, asteroids))

laser_scans = clockwise_scanned(x_max, y_max, width, height, asteroids)
left_to_shoot = [(len(scan), iter(scan)) for scan in laser_scans]

n_left = 200
while True:
    n_shot = min(el[0] for el in left_to_shoot)
    n_scans_left = len(left_to_shoot)
    n_together = n_shot * n_scans_left
    if n_together >= n_left:
        pos = n_left - 1
        scan_pos = pos % n_scans_left
        line_pos = pos // n_scans_left
        _, it = left_to_shoot[scan_pos]
        x_bet, y_bet = next(islice(it, line_pos, None))
        break

    left_to_shoot = [(n - n_shot, islice(it, n_shot, None))
                     for n, it in left_to_shoot if n > n_shot]
    n_left -= n_together

solution = 100 * x_bet + y_bet
print(solution)
