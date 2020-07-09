from utils.parse import Parser
from aoc.intcode import Machine
from copy import deepcopy
from collections import deque
from enum import Enum


class SendState(Enum):
    NOTHING_READ = 0
    DESTINATION_READ = 1
    X_READ = 2

    def __new__(cls, value):
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def advance(self):
        size = len(SendState)
        new_value = (self._value_ + 1) % size
        return SendState(new_value)


class Computer:
    def __init__(self, id, program, send_callback):
        self.__id = id
        self.__cpu = Machine(
            program, self.__receive_message, self.__send__message)
        self.__msg_queue = deque()
        self.__send_callback = send_callback
        self.__state = SendState.NOTHING_READ
        self.__booted = False

        self.__next_dest = None
        self.__next_x = None

        self.__state_map = {
            SendState.NOTHING_READ: self.__store_dest,
            SendState.DESTINATION_READ: self.__store_x,
            SendState.X_READ: self.__do_send
        }

    @property
    def halted(self):
        return self.__cpu.halted

    def step(self):
        self.__cpu.step()

    def queue_message(self, x, y):
        msg = x, y
        self.__msg_queue.extend(msg)

    def __send__message(self, value):
        self.__state_map[self.__state](value)
        self.__state = self.__state.advance()

    def __receive_message(self):
        if not self.__booted:
            self.__booted = True
            return self.__id

        if not self.__msg_queue:
            return -1

        next_value = self.__msg_queue.popleft()
        return next_value

    def __store_dest(self, value):
        self.__next_dest = value

    def __store_x(self, value):
        self.__next_x = value

    def __do_send(self, value):
        self.__send_callback(self.__next_dest, self.__next_x, value)


class Network:
    def __init__(self, program):
        self.__computers = [Computer(id, deepcopy(
            program), self.__send_message) for id in range(50)]
        self.__special_msg = None

    @property
    def special_msg(self):
        return self.__special_msg

    def run(self):
        while self.__special_msg is None:
            for c in self.__computers:
                c.step()

    def __send_message(self, dest, x, y):
        if dest == 255:
            if self.__special_msg is None:
                self.__special_msg = y
            return

        recipient = self.__computers[dest]
        recipient.queue_message(x, y)


parser = Parser("Day 23: Category Six - Part 1")
parser.parse()
with parser.input as input:
    line = input.readline()
    program = [int(el) for el in line.split(',')]

network = Network(program)
network.run()

print(network.special_msg)
