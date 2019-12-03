from utils.parse import Parser


class Grid:
    def __init__(self):
        self.__cells = set()
        self.__intersections = []

    def wire(self, direction, start, length):
        pass

    def reset_intersections(self):
        self.__intersections = []

    def __up(self, start, length):
        x_s, y_s = start
        for y in range(y_s + 1, y_s + length + 1):
            cell = x_s, y
            if cell in self.__cells:
                self.__intersections.append(cell)
            else:
                self.__cells.add(cell)

    def __down(self, start, length):
        x_s, y_s = start
        for y in range(y_s - 1, y_s - length - 1, -1):
            cell = x_s, y
            if cell in self.__cells:
                self.__intersections.append(cell)
            else:
                self.__cells.add(cell)

    def __left(self, start, length):
        x_s, y_s = start
        for x in range(x_s - 1, x_s - length - 1, -1):
            cell = x, y_s
            if cell in self.__cells:
                self.__intersections.append(cell)
            else:
                self.__cells.add(cell)

    def __right(self, start, length):
        x_s, y_s = start
        for x in range(x_s + 1, x_s + length + 1):
            cell = x, y_s
            if cell in self.__cells:
                self.__intersections.append(cell)
            else:
                self.__cells.add(cell)


parser = Parser()
with parser.input as input:
    line1 = input.readline()
    wire_a = [(path[:1], int(path[1:])) for path in line1.strip().split(',')]
    line2 = input.readline()
    wire_b = [(path[:1], int(path[1:])) for path in line2.strip().split(',')]
