from utils.parse import Parser
from itertools import islice, chain, repeat


def partial_sum_chain(data):
    current = 0
    yield current
    for n in data:
        current += n
        yield current


def calculate_phase(suffix):
    partial_chain = partial_sum_chain(reversed(suffix))
    digits = [abs(v) % 10 for v in partial_chain]
    digits.reverse()
    return digits


def phase_chain(data):
    current = data
    while True:
        current = calculate_phase(current)
        yield current


parser = Parser("Day 16: Flawed Frequency Transmission - Part 2")
parser.parse()
with parser.input as input:
    line = input.readline().strip()
    data = [int(el) for el in line]

# works based on the assumption
# that message offset lies in the second half of the data
message_offset = int(line[:7])

real_data = chain.from_iterable(repeat(data, 10000))
relevant_suffix = list(islice(real_data, message_offset, None))

bound_chain = islice(phase_chain(relevant_suffix), 100)
*_, solution = bound_chain

printed = "".join(map(str, solution[:8]))
print(printed)
