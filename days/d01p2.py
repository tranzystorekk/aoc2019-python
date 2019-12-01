from itertools import takewhile
from utils.parse import Parser


def fuel_req(mass):
    return mass // 3 - 2


def fuel_chain(initial_mass):
    current = fuel_req(initial_mass)
    while True:
        yield current
        current = fuel_req(current)


parser = Parser()
with parser.input as input:
    modules = [int(val) for val in input]

total_fuel = 0
for mass in modules:
    chain = fuel_chain(mass)
    valid_chain = takewhile(lambda m: m > 0, chain)
    total_fuel += sum(valid_chain)

print(total_fuel)
