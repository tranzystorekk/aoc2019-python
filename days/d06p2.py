from utils.parse import Parser
from itertools import groupby, dropwhile, zip_longest, tee, takewhile
from operator import itemgetter, truth

parser = Parser()
with parser.input as input:
    mappings = (l.strip().split(')') for l in input)
    orbit_map = [(grav, orb) for grav, orb in mappings]

orbit_map = sorted(orbit_map)
grouped = groupby(orbit_map, itemgetter(0))
gravs = {g: [o for _, o in orbs] for g, orbs in grouped}

# depth-first search
current_searchspace = [([], 'COM')]
santa_found = False
me_found = False
while current_searchspace:
    path, g = current_searchspace.pop()
    current_path = path + [g]
    orbiters = ((current_path, orb) for orb in gravs.get(g, []))
    current_searchspace.extend(orbiters)

    if g == 'SAN':
        santa_path = path
        santa_found = True
    elif g == 'YOU':
        me_path = path
        me_found = True

    if santa_found and me_found:
        break

zipped = zip_longest(me_path, santa_path)
divergent = dropwhile(lambda t: t[0] == t[1], zipped)

me_div, santa_div = tee(divergent)
me_div = takewhile(truth, map(itemgetter(0), me_div))
santa_div = takewhile(truth, map(itemgetter(1), santa_div))

me_transfers = sum(1 for _ in me_div)
santa_transfers = sum(1 for _ in santa_div)

print(me_transfers + santa_transfers)
