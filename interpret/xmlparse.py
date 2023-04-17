import xml.etree.ElementTree as ET
import sys
from errorCodes import ErrorCodes as ec, exitMessage
import re
from instructions import Instruction


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
        opcodes = {'MOVE': 2, 'CREATEFRAME': 0, 'PUSHFRAME': 0, 'POPFRAME': 0, 'DEFVAR': 1,
                   'CALL': 1, 'RETURN': 0, 'PUSHS': 1, 'POPS': 1, 'ADD': 3, 'SUB': 3, 'MUL': 3,
                   'IDIV': 3, 'LT': 3, 'GT': 3, 'EQ': 3, 'AND': 3, 'OR': 3, 'NOT': 2, 'INT2CHAR': 2,
                   'STRI2INT': 3, 'READ': 2, 'WRITE': 1, 'CONCAT': 3, 'STRLEN': 2, 'GETCHAR': 3,
                   'SETCHAR': 3, 'TYPE': 2, 'LABEL': 1, 'JUMP': 1, 'JUMPIFEQ': 3, 'JUMPIFNEQ': 3,
                   'EXIT': 1, 'DPRINT': 1, 'BREAK': 0}

        order = []

        try:
            xml = sorted(self.tree.findall('instruction'),
                         key=lambda x: int(x.attrib['order']))
        except ValueError:
            exitMessage(ec.INVALID_XML, "Invalid order")
        except KeyError:
            exitMessage(ec.INVALID_XML, "Invalid Keyword")

        for ele in self.tree.iter():
            if ele.tag not in ['program', 'instruction', 'arg1', 'arg2', 'arg3']:
                exitMessage(ec.INVALID_XML, "Invalid tag")

        for i, ins in enumerate(xml):
            i += 1
            try:
                if ins.attrib['opcode'].upper() not in opcodes.keys():
                    exitMessage(ec.INVALID_XML, "Invalid oppcode")
                if ins.attrib['order'].isdigit() is False or int(ins.attrib['order']) == 0 or int(ins.attrib['order']) in order:
                    exitMessage(ec.INVALID_XML, "Invalid order")
                order.append(int(ins.attrib['order']))
            except KeyError:
                exitMessage(ec.INVALID_XML, "Keyword missing")

            """Check number of arguments"""
            num_args = len(ins.findall('.//'))
            if num_args > 3:
                exitMessage(ec.INVALID_XML, "Invalid number of arguments")

            arg1 = ins.findall('arg1')
            arg2 = ins.findall('arg2')
            arg3 = ins.findall('arg3')

            # if len(arg1) > 1 or len(arg2) > 1 or len(arg3) > 1:
            #     exitMessage(ec.INVALID_XML, "Invalid number of arguments")
            # elif num_args != len(arg1) + len(arg2) + len(arg3):
            #     exitMessage(ec.INVALID_XML, "Invalid number of arguments")
            if num_args != opcodes[ins.attrib['opcode'].upper()]:
                exitMessage(ec.INVALID_XML, "Invalid number of arguments")

            if opcodes[ins.attrib['opcode'].upper()] == 0:
                if len(arg1) != 0 or len(arg2) != 0 or len(arg3) != 0:
                    exitMessage(ec.INVALID_XML, "Invalid number of arguments")
            elif opcodes[ins.attrib['opcode'].upper()] == 1:
                if len(arg1) != 1 or len(arg2) != 0 or len(arg3) != 0:
                    exitMessage(ec.INVALID_XML, "Invalid number of arguments")
            elif opcodes[ins.attrib['opcode'].upper()] == 2:
                if len(arg1) != 1 or len(arg2) != 1 or len(arg3) != 0:
                    exitMessage(ec.INVALID_XML, "Invalid number of arguments")
            elif opcodes[ins.attrib['opcode'].upper()] == 3:
                if len(arg1) != 1 or len(arg2) != 1 or len(arg3) != 1:
                    exitMessage(ec.INVALID_XML, "Invalid number of arguments")
            
            """Distribution of arguments"""
            if len(arg1) == 1:
                arg1 = arg1[0]
                if len(arg2) == 1:
                    arg2 = arg2[0]
                    if len(arg3) == 1:
                        arg3 = arg3[0]
                        try:
                            self.instructions.append([i, ins.attrib['opcode'],
                                                      arg1.attrib['type'], arg1.text.strip() if not arg1.text is None else None,
                                                      arg2.attrib['type'], arg2.text.strip() if not arg2.text is None else None,
                                                      arg3.attrib['type'], arg3.text.strip() if not arg3.text is None else None])
                        except:
                            print(i, ins.attrib['opcode'], arg1.attrib['type'])
                            # print(xml)
                            # exitMessage(ec.INVALID_XML)
                    else:
                        self.instructions.append([i, ins.attrib['opcode'],
                                                  arg1.attrib['type'], arg1.text.strip() if not arg1.text is None else None,
                                                  arg2.attrib['type'], arg2.text.strip() if not arg2.text is None else None])
                else:
                    self.instructions.append([i, ins.attrib['opcode'],
                                              arg1.attrib['type'], arg1.text.strip() if not arg1.text is None else None])
            else:
                self.instructions.append([i, ins.attrib['opcode']])

        return self.instructions


if __name__ == '__main__':
    parser = Parse()
