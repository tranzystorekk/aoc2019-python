from utils.parse import Parser
from itertools import combinations
from operator import itemgetter


class Vector:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    @property
    def tuple(self):
        return self.x, self.y, self.z

    @property
    def energy(self):
        return abs(self.x) + abs(self.y) + abs(self.z)

    def apply(self, vec):
        self.x += vec.x
        self.y += vec.y
        self.z += vec.z


class Moon:
    def __init__(self, pos):
        self.__pos = pos
        self.__velocity = Vector()

    @property
    def position(self):
        return self.__pos.tuple

    @property
    def total_energy(self):
        return self.__pos.energy * self.__velocity.energy

    def apply_gravity(self, gravity):
        self.__velocity.apply(gravity)

    def apply_velocity(self):
        self.__pos.apply(self.__velocity)


def axis_gravity(a, b):
    if a < b:
        return 1, -1

    elif a > b:
        return -1, 1

    return 0, 0


def do_time_step(moons):
    for moon_a, moon_b in combinations(moons, 2):
        gravity = [axis_gravity(c_a, c_b) for c_a, c_b in zip(moon_a.position, moon_b.position)]
        grav_a = Vector(*map(itemgetter(0), gravity))
        grav_b = Vector(*map(itemgetter(1), gravity))
        moon_a.apply_gravity(grav_a)
        moon_b.apply_gravity(grav_b)

    for m in moons:
        m.apply_velocity()


parser = Parser("Day 12: The N-Body Problem - Part 1")
parser.parse()
with parser.input as input:
    stripped = (l.strip('<>\n') for l in input)
    coordinates = (l.split(',') for l in stripped)
    moons = []
    for moon in coordinates:
        values = (coord.strip('xyz= ') for coord in moon)
        position = Vector(*map(int, values))
        moons.append(Moon(position))

for _ in range(1000):
    do_time_step(moons)

total_energy = sum(m.total_energy for m in moons)

print(total_energy)
