import xml.etree.ElementTree as ET
import sys
from errorCodes import ErrorCodes as ec, exitMessage
import re


class Parse:
    def __init__(self):
        self.tree = None
        self.instructions = []

    def parse(self, source):
        try:
            self.tree = ET.parse(source)
        except ET.ParseError:
            exitMessage(ec.MALFORMED_XML, "Malformed XML")
        except FileNotFoundError:
            exitMessage(ec.INPUT_FILE_ERROR, "Input file error")
        except:
            exitMessage(ec.INTERNAL_ERROR, "Internal error")

        self.root = self.tree.getroot()
        self._checkRoot()
        return self._checkInstructions()

    def _checkRoot(self):
        if (self.root.tag != 'program'
                or 'language' not in self.root.attrib
                or self.root.attrib['language'] != 'IPPcode23'):
            exitMessage(ec.INVALID_XML, "Invalid attribute")

    def _checkInstructions(self):
        opcodes = ['MOVE', 'CREATEFRAME', 'PUSHFRAME', 'POPFRAME', 'DEFVAR', 'CALL', 'RETURN', 'PUSHS', 'POPS', 'ADD',
                   'SUB', 'MUL', 'IDIV', 'LT', 'GT', 'EQ', 'AND', 'OR', 'NOT', 'INT2CHAR', 'STRI2INT', 'READ', 'WRITE',
                   'CONCAT', 'STRLEN', 'GETCHAR', 'SETCHAR', 'TYPE', 'LABEL', 'JUMP', 'JUMPIFEQ', 'JUMPIFNEQ', 'EXIT',
                   'DPRINT', 'BREAK']
        
        try:
            xml = sorted(self.tree.findall('instruction'), key=lambda x: int(x.attrib['order']))
        except ValueError:
            exitMessage(ec.INVALID_XML, "Invalid order")
        except KeyError:
            exitMessage(ec.INVALID_XML, "Invalid Keyword")

        for i,ins in enumerate(xml):
            i += 1
            if ins.attrib['opcode'] not in opcodes:
                exitMessage(ec.INVALID_XML, "Invalid oppcode")
            if ins.attrib['order'].isdigit() is False:
                exitMessage(ec.INVALID_XML, "Invalid order")

            arg1 = ins.findall('arg1')
            arg2 = ins.findall('arg2')
            arg3 = ins.findall('arg3')

            if len(arg1) > 1 or len(arg2) > 1 or len(arg3) > 1:
                exitMessage(ec.INVALID_XML, "Invalid number of arguments")

            if len(arg1) == 1:
                arg1 = arg1[0]
                if len(arg2) == 1:
                    arg2 = arg2[0]
                    if len(arg3) == 1:
                        arg3 = arg3[0]
                        self.instructions.append([i, ins.attrib['opcode'], 
                                                  arg1.attrib['type'], arg1.text.strip(), 
                                                  arg2.attrib['type'], arg2.text.strip(), 
                                                  arg3.attrib['type'], arg3.text.strip()])
                    else:
                        self.instructions.append([i, ins.attrib['opcode'], 
                                                  arg1.attrib['type'], arg1.text.strip(), 
                                                  arg2.attrib['type'], arg2.text.strip()])
                else:
                    self.instructions.append([i, ins.attrib['opcode'], 
                                              arg1.attrib['type'], arg1.text.strip()])


        return self.instructions


if __name__ == '__main__':
    parser = Parse()
