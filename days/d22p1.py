from utils.parse import Parser
from itertools import islice, chain, count
from enum import Enum


class Operation(Enum):
    DEAL_STACK = 0
    CUT = 1
    DEAL_INCREMENT = 2


class Args:
    def __init__(self, dict=None):
        if dict is not None:
            self.__dict__.update(dict)


def parse_instruction(s):
    head, tail = s.rsplit(maxsplit=1)

    try:
        value = int(tail)
    except ValueError:
        return Operation.DEAL_STACK, Args()

    args = {'value': value}
    op = Operation.DEAL_INCREMENT
    if head == 'cut':
        op = Operation.CUT

    return op, Args(args)


def deal_stack(deck, args):
    return list(reversed(deck))


def cut(deck, args):
    partition = args.value
    if partition < 0:
        partition += len(deck)

    tail = islice(deck, partition, None)
    head = islice(deck, partition)
    chained = chain(tail, head)

    return list(chained)


def deal_increment(deck, args):
    incr = args.value
    size = len(deck)
    indices = (i % size for i in count(step=incr))
    result = [None for _ in deck]
    for ind, v in zip(indices, deck):
        result[ind] = v

    return result


parser = Parser()
parser.parse()
with parser.input as input:
    lines = (line.strip() for line in input)
    mapped = [parse_instruction(s) for s in lines]

op_mappings = {
    Operation.DEAL_STACK: deal_stack,
    Operation.CUT: cut,
    Operation.DEAL_INCREMENT: deal_increment
}

deck = list(range(10007))
for op, args in mapped:
    deck = op_mappings[op](deck, args)

solution = deck.index(2019)

print(solution)
