from utils.parse import Parser
from itertools import groupby
from operator import itemgetter

parser = Parser("Day 6: Universal Orbit Map - Part 1")
with parser.input as input:
    mappings = (l.strip().split(')') for l in input)
    orbit_map = [(grav, orb) for grav, orb in mappings]

orbit_map = sorted(orbit_map)
grouped = groupby(orbit_map, itemgetter(0))
gravs = {g: [o for _, o in orbs] for g, orbs in grouped}

# depth-first search
current_searchspace = [(0, 'COM')]
total_orbits = 0
while current_searchspace:
    level, g = current_searchspace.pop()
    total_orbits += level
    current_level = level + 1
    orbiters = ((current_level, orb) for orb in gravs.get(g, []))
    current_searchspace.extend(orbiters)

print(total_orbits)
