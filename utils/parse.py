import sys
from argparse import ArgumentParser, FileType

class Parser:
    def __init__(self, desc=None):
        parser = ArgumentParser(description=desc)
        parser.add_argument("infile", nargs="?", type=FileType('r'), default=sys.stdin, metavar="FILEPATH", \
                            help="Input file path, default: STDIN")
        self.__args = parser.parse_args()

    @property
    def input(self):
        return self.__args.infile
