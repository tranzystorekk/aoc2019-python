from utils.parse import Parser


def fuel_req(mass):
    return mass // 3 - 2


parser = Parser()
with parser.input as input:
    modules = [int(val) for val in input]

total_fuel = sum(fuel_req(m) for m in modules)
print(total_fuel)
