from arguments import *
from enum import Enum
import sys
from errorCodes import ErrorCodes as ec, exitMessage
from xmlparse import Parse
from frames import Frame




class Main:
    def __init__(self):
        self.args = arguments()
        args = self.args.getArgs()

        self.XML = Parse()
        instructions = self.XML.parse(args.source)
        
        for instruction in instructions:
            print(instruction)

        self.t_frame = None
        self.g_frame = Frame()
        self.l_frame = []
        self.data_stack = []
        self.call_stack = []
        self.labels = {}

if __name__ == '__main__':
    Main()

# sorted metoda nekde u xml knihovny
