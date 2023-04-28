from arguments import *
from enum import Enum
import sys
from errorCodes import ErrorCodes as ec, exitMessage
from xmlparse import Parse
from frames import Frame
from instructions import *
from run import Run


class Main:
    def __init__(self):
        self.lineArgs = parseArguments()
        lineArgs = self.lineArgs.getArgs()

        self.XML = Parse()
        instructions = [Instruction(instruction)
                        for instruction in self.XML.parse(lineArgs.source)]

        self.run = Run(instructions, lineArgs)


if __name__ == '__main__':
    Main()
