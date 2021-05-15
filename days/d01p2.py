from itertools import takewhile
from utils.parse import Parser


def successors(start, func):
    next = start
    while True:
        yield next
        next = func(next)


def fuel_req(mass):
    return mass // 3 - 2


def fuel_req_chained(initial_mass):
    start = fuel_req(initial_mass)
    chain = successors(start, fuel_req)
    valid_chain = takewhile(lambda val: val > 0, chain)
    return sum(valid_chain)


parser = Parser("Day 1: The Tyranny of the Rocket Equation - Part 2")
parser.parse()
with parser.input as input:
    modules = [int(val) for val in input]

total_fuel = sum(fuel_req_chained(v) for v in modules)

print(total_fuel)
