from utils.parse import Parser, FileType
from aoc.intcode import Machine


class VacuumRobot:
    def __init__(self, program, routine):
        self.__cpu = Machine(program, self.__get_routine, self.__get_dust)
        self.__routine = routine
        self.__it = iter(self.__routine)
        self.__dust_amount = None

    @property
    def dust_amount(self):
        return self.__dust_amount

    def run(self):
        self.__cpu.run()

    def __get_routine(self):
        c = next(self.__it)
        return ord(c)

    def __get_dust(self, value):
        self.__dust_amount = value


# use misc.d17path to obtain the path and then manually divide it into routines
parser = Parser("Day 17: Set and Forget - Part 2")
parser.add_argument("--routine", type=FileType('r'), metavar="ROUTINE", required=True,
                    help="File with movement routine description")
parser.parse()
with parser.input as input, parser.routine as routine:
    line = input.readline()
    program = [int(el) for el in line.split(',')]

    routines = routine.read()

program[0] = 2
robot = VacuumRobot(program, routines)
robot.run()

print(robot.dust_amount)
