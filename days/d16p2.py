from utils.parse import Parser
from itertools import count, takewhile, cycle, islice, chain, repeat


def flatten(list_of_lists):
    "Flatten one level of nesting"
    return chain.from_iterable(list_of_lists)


def partial_sum_chain(data):
    current = 0
    yield current
    for n in data:
        current += n
        yield current


def segments(size):
    result = ((i - 1, i + size - 1) for i in count(size, 2 * size))
    return result


def calculate_digit(partial_sums, pos):
    size = len(partial_sums)
    segment_size = pos + 1
    bound_segments = takewhile(lambda p: p[0] < size, segments(segment_size))
    upper_limited = ((beg, end if end < size else size - 1) for beg, end in bound_segments)
    segment_sums = (partial_sums[end] - partial_sums[beg] for beg, end in upper_limited)
    multipliers = cycle([1, -1])
    calculated = sum(v * m for v, m in zip(segment_sums, multipliers))
    return abs(calculated) % 10


def calculate_phase(data):
    partial_sums = list(partial_sum_chain(data))
    size = len(partial_sums)
    return [calculate_digit(partial_sums, pos) for pos in range(size)]


def phase_chain(data):
    current = data
    n = 1
    while True:
        print(n)
        n += 1
        current = calculate_phase(current)
        yield current


parser = Parser()
with parser.input as input:
    line = input.readline().strip()
    data = [int(el) for el in line]

message_offset = int(line[:7])

real_data = list(flatten(repeat(data, 10000)))

bound_chain = islice(phase_chain(real_data), 100)
*_, solution = bound_chain

printed = "".join(map(str, solution[message_offset:message_offset + 8]))
print(printed)
