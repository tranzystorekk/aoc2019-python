import sys
from argparse import ArgumentParser

class Parser:
    def __init__(self, desc=None):
        parser = ArgumentParser(description=desc)
        parser.add_argument("-f", "--file", default=None, metavar="FILEPATH", \
                            help="Input file path, defaults to stdin if this flag is not specified")
        self.__args = parser.parse_args()

    def input(self):
        inp = sys.stdin
        if (file:=self.__args.file):
            inp = open(file)

        return inp
