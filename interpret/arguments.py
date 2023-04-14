import argparse
from errorCodes import ErrorCodes as ec, exitMessage
import sys


class parseArguments:
    def __init__(self):
        self.args = None

    def getArgs(self):
        self.parser = argparse.ArgumentParser(
            usage='python interpret.py [--help] [--source=file] [--input=file]\n\n\
                    \tAt least one of the arguments --source or --input is required\n\
                    \tIf one is missing, script reads from STDIN\n ', add_help=False)
        self.parser.add_argument(
            '--help', action="store_true", help="Output help and exit")
        self.parser.add_argument(
            '--source', help="XML file to interpret (if not specified reads from STDIN)", required=False)
        self.parser.add_argument(
            '--input', help="Input file (if not specified reads from STDIN)", required=False)

        try:
            self.args = self.parser.parse_args()
        except argparse.ArgumentError:
            exitMessage(ec.MISSING_ARGUMENT, "Invalid arguments")
        except SystemExit:
            exitMessage(ec.MISSING_ARGUMENT, "Invalid arguments")

        return self._checkArgs()

    def _checkArgs(self):
        if self.args.help and len(sys.argv) > 2:
            exitMessage(ec.MISSING_ARGUMENT, "Invalid arguments")

        elif self.args.help:
            self.parser.print_help()
            exitMessage(ec.OK)

        elif self.args.source and self.args.input is None:
            self.args.input = sys.stdin

            try:
                self.args.source = open(self.args.source, 'r')
            except FileNotFoundError:
                exitMessage(ec.INPUT_FILE_ERROR, "Input file error")

        elif self.args.source is None and self.args.input:
            self.args.source = sys.stdin

            try:
                self.args.input = open(self.args.input, 'r')
            except FileNotFoundError:
                exitMessage(ec.INPUT_FILE_ERROR, "Input file error")

        elif self.args.source is None and self.args.input is None:
            exitMessage(ec.MISSING_ARGUMENT,
                        "At least one of the arguments --source or --input is required")
            
        else:
            try:
                self.args.source = open(self.args.source, 'r')
                self.args.input = open(self.args.input, 'r')
            except FileNotFoundError:
                exitMessage(ec.INPUT_FILE_ERROR, "Input file error")
        
        return self.args

if __name__ == '__main__':
    parseArguments()
