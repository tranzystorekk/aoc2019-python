from utils.parse import Parser
from itertools import islice, repeat, chain, cycle


def get_pattern(position):
    base = [0, 1, 0, -1]
    repeats = (repeat(n, position + 1) for n in base)
    repeated = chain(*repeats)
    cycled = cycle(repeated)
    return islice(cycled, 1, None)


def compute_phase(data):
    size = len(data)
    calculated = (sum(n * p for n, p in zip(data, get_pattern(pos)))
                  for pos in range(size))
    output = [abs(n) % 10 for n in calculated]
    return output


def phases(initial_data):
    current = initial_data
    while True:
        current = compute_phase(current)
        yield current


parser = Parser("Day 16: Flawed Frequency Transmission - Part 1")
parser.parse()
with parser.input as input:
    line = input.readline().strip()
    data = [int(el) for el in line]

bound_chain = islice(phases(data), 100)
*_, result = bound_chain

printed = "".join(map(str, result[:8]))
print(printed)
