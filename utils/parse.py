import sys
from argparse import ArgumentParser, FileType


class Parser(ArgumentParser):
    def __init__(self, desc=None):
        super().__init__(description=desc)
        self.add_argument("input", nargs="?", type=FileType('r'), default=sys.stdin, metavar="FILEPATH",
                          help="Input file path, default: STDIN")

    def parse(self):
        args = self.parse_args()
        self.__dict__.update(vars(args))
