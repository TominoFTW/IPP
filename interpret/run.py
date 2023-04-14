from errorCodes import ErrorCodes as ec, exitMessage
from frames import Frame, Nil
import sys
from instructions import Argument
import re


class Run:
    def __init__(self, instructions, lineArgs):
        self.instructions = instructions
        self.lineArgs = lineArgs

        self.g_frame = Frame()
        self.l_frame = []
        self.t_frame = None

        self.data_stack = []
        self.call_stack = []
        self.instruction_pointer = 1
        self.order = 1

        self.labels = {}

        self.VAR = ['var']
        self.SYMB = ['var', 'int', 'bool', 'string', 'nil', 'var']
        self.LABEL = ['label']
        self.TYPE = ['int', 'bool', 'string', 'nil']
        
        self.run()

    def run(self):
        for instruction in self.instructions:
            # print("starting ",self.instruction_pointer)
            if instruction.opcode == "MOVE":
                self._move(instruction)
            elif instruction.opcode == "CREATEFRAME":
                self._createframe(instruction)
            elif instruction.opcode == "PUSHFRAME":
                self._pushframe(instruction)
            elif instruction.opcode == "POPFRAME":
                self._popframe(instruction)
            elif instruction.opcode == "DEFVAR":
                self._defvar(instruction)
            elif instruction.opcode == "CALL":
                self._call(instruction)
            elif instruction.opcode == "RETURN":
                self._return(instruction)
            elif instruction.opcode == "PUSHS":
                self._pushs(instruction)
            elif instruction.opcode == "POPS":
                self._pops(instruction)
            elif instruction.opcode == "ADD":
                self._add(instruction)
            elif instruction.opcode == "SUB":
                self._sub(instruction)
            elif instruction.opcode == "MUL":
                self._mul(instruction)
            elif instruction.opcode == "IDIV":
                self._idiv(instruction)
            elif instruction.opcode == "LT":
                self._lt(instruction)
            elif instruction.opcode == "GT":
                self._gt(instruction)
            elif instruction.opcode == "EQ":
                self._eq(instruction)
            elif instruction.opcode == "AND":
                self._and(instruction)
            elif instruction.opcode == "OR":
                self._or(instruction)
            elif instruction.opcode == "NOT":
                self._not(instruction)
            elif instruction.opcode == "INT2CHAR":
                self._int2char(instruction)
            elif instruction.opcode == "STRI2INT":
                self._stri2int(instruction)
            elif instruction.opcode == "READ":
                self._read(instruction)
            elif instruction.opcode == "WRITE":
                # print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                self._write(instruction)
                # print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            elif instruction.opcode == "CONCAT":
                self._concat(instruction)
            elif instruction.opcode == "STRLEN":
                self._strlen(instruction)
            elif instruction.opcode == "GETCHAR":
                self._getchar(instruction)
            elif instruction.opcode == "SETCHAR":
                self._setchar(instruction)
            elif instruction.opcode == "TYPE":
                self._type(instruction)
            elif instruction.opcode == "LABEL":
                self._label(instruction)
            elif instruction.opcode == "JUMP":
                self._jump(instruction)
            elif instruction.opcode == "JUMPIFEQ":
                self._jumpifeq(instruction)
            elif instruction.opcode == "JUMPIFNEQ":
                self._jumpifneq(instruction)
            elif instruction.opcode == "EXIT":
                self._exit(instruction)
            elif instruction.opcode == "DPRINT":
                self._dprint(instruction)
            elif instruction.opcode == "BREAK":
                self._break(instruction)
            else:
                exitMessage(ec.INVALID_XML, "Invalid oppcode")

            # print("\n",self.instruction_pointer,"___",end=" ")
            # print(self.g_frame.get_frame())
            self.instruction_pointer += 1


    def _move(self, instruction):
        self.args = instruction.args
        if self.args[0].type == 'var' and self.args[1].type in self.SYMB:
            try:
                if self.args[1].type == 'var': # var var
                        frame1,_  = self.args[0].value.split('@', 1)
                        _, name2 = self.args[1].value.split('@', 1)
                        if frame1 == 'GF':
                            value = self.g_frame.set_var(self.g_frame.get_var_value(name2))
                        elif frame1 == 'TF':
                            value = self.t_frame.get_var(self.t_frame.get_var_value(name2))
                        elif frame1 == 'LF':
                            value = self.l_frame[-1].get_var(self.l_frame[-1].get_var_value(name2))
                        else:
                            exitMessage(ec.INVALID_XML, "Invalid frame")
                else:   # var (int, bool, string, nil)
                    value = self.args[1].value
                    type = self.args[1].type
                    # print("::::::::::",value,type,sep=" ")
                    frame, name = self.args[0].value.split('@', 1)
                    if frame == 'GF':
                        self.g_frame.set_var_type(name, value, type)
                    elif frame == 'TF':
                        self.t_frame.set_var_type(name, value, type)
                    elif frame == 'LF':
                        self.l_frame[-1].set_var_type(name, value, type)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
            except IndexError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
            except AttributeError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")

    
    def _createframe(self, instruction):
        self.t_frame = Frame()

    def _pushframe(self, instruction):
        if self.t_frame is not None:
            self.l_frame.append(self.t_frame)
            self.t_frame = None
        else:
            exitMessage(ec.INVALID_FRAME, "Missing value in frame")

    def _popframe(self, instruction):
        try:
            self.t_frame = self.l_frame.pop()
        except IndexError:
            exitMessage(ec.INVALID_FRAME, "Missing value in frame")

    def _defvar(self, instruction):
        self.args = instruction.args
        if self.args[0].type == 'var':
            try:
                frame, name = self.args[0].value.split('@', 1)
                if frame == 'GF':
                    self.g_frame.def_var(name)
                elif frame == 'TF':
                    self.t_frame.def_var(name)
                elif frame == 'LF':
                    self.l_frame[-1].def_var(name)
                else:
                    exitMessage(ec.INVALID_XML, "Invalid frame")
            except IndexError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
            except AttributeError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
        else:
            exitMessage(ec.INVALID_XML, "Invalid argument type")

    def _call(self, instruction):
        # print(instruction.opcode)
        pass

    def _return(self, instruction):
        # print(instruction.opcode)
        pass

    def _pushs(self, instruction):
        # print(instruction.opcode)
        pass

    def _pops(self, instruction):
        # print(instruction.opcode)
        pass

    def _add(self, instruction):
        # print(instruction.opcode)
        pass

    def _sub(self, instruction):
        # print(instruction.opcode)
        pass

    def _mul(self, instruction):
        # print(instruction.opcode)
        pass

    def _idiv(self, instruction):
        # print(instruction.opcode)
        pass

    def _lt(self, instruction):
        # print(instruction.opcode)
        pass

    def _gt(self, instruction):
        # print(instruction.opcode)
        pass

    def _eq(self, instruction):
        # print(instruction.opcode)
        pass

    def _and(self, instruction):
        # print(instruction.opcode)
        pass

    def _or(self, instruction):
        # print(instruction.opcode)
        pass

    def _not(self, instruction):
        # print(instruction.opcode)
        pass

    def _int2char(self, instruction):
        # print(instruction.opcode)
        pass


    def _stri2int(self, instruction):
        # print(instruction.opcode)
        pass

    def _read(self, instruction):
        # print(instruction.opcode)
        pass

    def _write(self, instruction):
        self.args = instruction.args
        if self.args[0].type == 'var':
            try:
                frame, name = self.args[0].value.split('@', 1)
                if frame == 'GF':
                    self.g_frame.write_var(name)
                elif frame == 'TF':
                    self.t_frame.write_var(name)
                elif frame == 'LF':
                    self.l_frame[-1].write_var(name)
                else:
                    exitMessage(ec.INVALID_XML, "Invalid frame")
            except IndexError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
            except AttributeError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
        elif self.args[0].type in self.SYMB:
            if self.args[0].type == type(bool()):
                print(self.args[0].value.lower(), end='')
            elif self.args[0].type == Nil() or self.args[0].type == 'nil':    
                print("", end='')
            else:
                print(self.args[0].value, end='')
        
        else:
            exitMessage(ec.INVALID_XML, "Invalid argument type")


    def _concat(self, instruction):
        # print(instruction.opcode)
        pass

    def _strlen(self, instruction):
        # print(instruction.opcode)
        pass

    def _getchar(self, instruction):
        # print(instruction.opcode)
        pass

    def _setchar(self, instruction):
        # print(instruction.opcode)
        pass

    def _type(self, instruction):
        self.args = instruction.args
        if self.args[0].type == 'var' and self.args[1].type in self.SYMB:
            try:
                frame, name = self.args[0].value.split('@', 1)
                if self.args[1].type == 'var': # var var
                    _, name2 = self.args[1].value.split('@', 1)
                    if frame == 'GF':
                        self.g_frame.set_var(name, self.g_frame.get_var_type_str(name2))
                    elif frame == 'TF':
                        self.t_frame.set_var(name, self.t_frame.get_var_type_str(name2))
                    elif frame == 'LF':
                        self.l_frame[-1].set_var(name, self.l_frame[-1].get_var_type_str(name2))
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                else:           # var (int, bool, string, nil)
                    typ = self.args[1].type
                    if frame == 'GF':
                        self.g_frame.set_var(name, typ)
                    elif frame == 'TF':
                        self.t_frame.set_var(name, typ)
                    elif frame == 'LF':
                        self.l_frame[-1].set_var(name, typ)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
            except IndexError:
                exitMessage(ec.INVALID_FRAME, "Invalid frameERROR")
            except AttributeError:
                exitMessage(ec.INVALID_FRAME, "Invalid frameERROR")
        else:
            exitMessage(ec.INVALID_XML, "Invalid argument type")

    def _label(self, instruction):
        # print(instruction.opcode)
        pass

    def _jump(self, instruction):
        # print(instruction.opcode)
        pass

    def _jumpifeq(self, instruction):
        # print(instruction.opcode)
        pass


    def _jumpifneq(self, instruction):
        # print(instruction.opcode)
        pass

    def _exit(self, instruction):
        # print(instruction.opcode)
        pass

    def _dprint(self, instruction):
        # print(instruction.opcode)
        pass

    def _break(self, instruction):
        # print(instruction.opcode)
        pass
