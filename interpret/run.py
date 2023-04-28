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
        self.instruction_pointer = 0

        self.labels = {}

        self.SYMB = ['var', 'int', 'bool', 'string', 'nil', 'var']
        self.LABEL = ['label']
        self.TYPE = ['int', 'bool', 'string', 'nil']
        
        """ Check for duplicate labels """
        self.labels = {i:instruction.args[0].value for i, instruction in enumerate(self.instructions) 
                       if instruction.opcode == "LABEL" 
                       and instruction.args[0].value not in self.labels.values()}
        seen_values = []
        for value in self.labels.values():
            if value in seen_values:
                exitMessage(ec.SEMANTIC_ERROR, "Duplicate label")
            seen_values.append(value)

        self.labels = {v: k for k, v in self.labels.items()}

        self.run()

    def run(self):
        while (self.instruction_pointer < len(self.instructions)):
            try:
                instruction = self.instructions[self.instruction_pointer]
            except:
                exitMessage(ec.INTERNAL_ERROR)
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
                self._read(instruction, self.lineArgs.input)
            elif instruction.opcode == "WRITE":
                self._write(instruction)
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

            self.instruction_pointer += 1


    def _move(self, instruction):
        self.args = instruction.args
        if self.args[0].type == 'var' and self.args[1].type in self.SYMB:
            try:
                if self.args[1].type == 'var': # var var
                        frame2, name2 = self.args[1].value.split('@', 1)
                        if frame2 == 'GF':
                            val = self.g_frame.get_var_value(name2)
                            typ = self.g_frame.get_var_type(name2)
                        elif frame2 == 'TF':
                            val = self.t_frame.get_var_value(name2)
                            typ = self.t_frame.get_var_type(name2)
                        elif frame2 == 'LF':
                            val = self.l_frame[-1].get_var_value(name2)
                            typ = self.l_frame[-1].get_var_type(name2)
                        else:
                            exitMessage(ec.INVALID_XML, "Invalid frame")
                else:   # var (int, bool, string, nil)
                    val = self.args[1].value
                    typ = self.args[1].type
                if val == None and typ == 'string':
                    val = ''
                frame, name = self.args[0].value.split('@', 1)
                if frame == 'GF':
                    self.g_frame.set_var_type(name, val, typ)
                elif frame == 'TF':
                    self.t_frame.set_var_type(name, val, typ)
                elif frame == 'LF':
                    self.l_frame[-1].set_var_type(name, val, typ)
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
            exitMessage(ec.INVALID_XML, "Invalid XML things")

    def _call(self, instruction):
        self.args = instruction.args
        if self.args[0].type == 'label':
            try:
                if self.args[0].value not in self.labels.keys():
                    exitMessage(ec.SEMANTIC_ERROR, "Label not found")
                self.call_stack.append(self.instruction_pointer)
                self.instruction_pointer = self.labels[self.args[0].value]
            except KeyError:
                exitMessage(ec.INVALID_XML, "Invalid label")
        else:
            exitMessage(ec.INVALID_XML, "Invalid XML things")

    def _return(self, instruction):
        try:
            self.instruction_pointer = self.call_stack.pop()
        except IndexError:
            exitMessage(ec.MISSING_VALUE, "Invalid return")

    def _pushs(self, instruction):
        if instruction.args[0].type in self.SYMB:
            if instruction.args[0].type == 'var':
                try:
                    frame, name = instruction.args[0].value.split('@', 1)
                    if frame == 'GF':
                        self.data_stack.append((self.g_frame.get_var_value(name), self.g_frame.get_var_type_str(name)))
                    elif frame == 'TF':
                        self.data_stack.append((self.t_frame.get_var_value(name), self.t_frame.get_var_type_str(name)))
                    elif frame == 'LF':
                        self.data_stack.append((self.l_frame[-1].get_var_value(name), self.l_frame[-1].get_var_type_str(name)))
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                except IndexError:
                    exitMessage(ec.INVALID_FRAME, "Invalid frame")
                except AttributeError:
                    exitMessage(ec.INVALID_FRAME, "Invalid frame")
            else:
                try:
                    if instruction.args[0].value == None and instruction.args[0].type == 'string':
                        self.data_stack.append(('',instruction.args[0].type))
                    elif instruction.args[0].type == 'int':
                        self.data_stack.append((int(instruction.args[0].value), instruction.args[0].type))
                    elif instruction.args[0].type == 'bool':
                        self.data_stack.append((instruction.args[0].value.lower(), instruction.args[0].type))
                    else:
                        self.data_stack.append((instruction.args[0].value,instruction.args[0].type))
                except ValueError:
                    exitMessage(ec.INVALID_XML, "Invalid XML things")
        else:
            exitMessage(ec.INVALID_XML, "Invalid XML things")

    def _pops(self, instruction):
        if not self.data_stack:
            exitMessage(ec.MISSING_VALUE, "Invalid argument type")
        if instruction.args[0].type == 'var':
            value, typ = self.data_stack.pop()
            try:
                frame, name = instruction.args[0].value.split('@', 1)
                if frame == 'GF':
                    self.g_frame.set_var_type(name, value, typ)
                elif frame == 'TF':
                    self.t_frame.set_var_type(name, value, typ)
                elif frame == 'LF':
                    self.l_frame[-1].set_var_type(name, value, typ)
                else:
                    exitMessage(ec.INVALID_XML, "Invalid frame")
            except IndexError as e:
                exitMessage(ec.INVALID_FRAME, e)
            except AttributeError as e:
                exitMessage(ec.INVALID_FRAME, e)

    def _add(self, instruction):
        self.args = instruction.args
        if self.args[0].type == 'var' and self.args[1].type in self.SYMB and self.args[2].type in self.SYMB:
            try:
                if self.args[1].type == 'var':
                    frame1, name1 = self.args[1].value.split('@', 1)
                    if frame1 == 'GF':
                        val1 = self.g_frame.get_var_value(name1)
                    elif frame1 == 'TF':
                        val1 = self.t_frame.get_var_value(name1)
                    elif frame1 == 'LF':
                        val1 = self.l_frame[-1].get_var_value(name1)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                elif self.args[1].type == 'int':
                    try:
                        val1 = int(self.args[1].value)
                    except ValueError:
                        exitMessage(ec.INVALID_XML, "Invalid XML things")
                else:
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")

                if self.args[2].type == 'var':
                    frame2, name2 = self.args[2].value.split('@', 1)
                    if frame2 == 'GF':
                        val2 = self.g_frame.get_var_value(name2)
                    elif frame2 == 'TF':
                        val2 = self.t_frame.get_var_value(name2)
                    elif frame2 == 'LF':
                        val2 = self.l_frame[-1].get_var_value(name2)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                elif self.args[2].type == 'int': 
                    # print("tu2")
                    try:
                        val2 = int(self.args[2].value)
                    except ValueError:
                        exitMessage(ec.INVALID_XML, "Invalid XML things")
                else:
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")

                if type(val1) != type(int()) or type(val2) != type(int()):
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                if val1 is None or val2 is None:
                    exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                    
                frame, name = self.args[0].value.split('@', 1)
                if frame == 'GF':
                    self.g_frame.set_var(name, val1 + val2)
                elif frame == 'TF':
                    self.t_frame.set_var(name, val1 + val2)
                elif frame == 'LF':
                    self.l_frame[-1].set_var(name, val1 + val2)
                else:
                    exitMessage(ec.INVALID_XML, "Invalid frame")
            except IndexError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
            except AttributeError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
        else:
            exitMessage(ec.INVALID_XML, "Invalid XML things")

    def _sub(self, instruction):
        self.args = instruction.args
        if self.args[0].type == 'var' and self.args[1].type in self.SYMB and self.args[2].type in self.SYMB:
            try:
                if self.args[1].type == 'var':
                    frame1, name1 = self.args[1].value.split('@', 1)
                    if frame1 == 'GF':
                        val1 = self.g_frame.get_var_value(name1)
                    elif frame1 == 'TF':
                        val1 = self.t_frame.get_var_value(name1)
                    elif frame1 == 'LF':
                        val1 = self.l_frame[-1].get_var_value(name1)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                elif self.args[1].type == 'int':
                     
                    val1 = int(self.args[1].value)
                else:
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")

                if self.args[2].type == 'var':
                    frame2, name2 = self.args[2].value.split('@', 1)
                    if frame2 == 'GF':
                        val2 = self.g_frame.get_var_value(name2)
                    elif frame2 == 'TF':
                        val2 = self.t_frame.get_var_value(name2)
                    elif frame2 == 'LF':
                        val2 = self.l_frame[-1].get_var_value(name2)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                elif self.args[2].type == 'int': 
                    val2 = int(self.args[2].value)
                else:
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")

                if type(val1) != type(int()) or type(val2) != type(int()):
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                if val1 is None or val2 is None:
                    exitMessage(ec.MISSING_VALUE, "Invalid argument type")

                frame, name = self.args[0].value.split('@', 1)
                if frame == 'GF':
                    self.g_frame.set_var(name, val1 - val2)
                elif frame == 'TF':
                    self.t_frame.set_var(name, val1 - val2)
                elif frame == 'LF':
                    self.l_frame[-1].set_var(name, val1 - val2)
                else:
                    exitMessage(ec.INVALID_XML, "Invalid frame")
            except IndexError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
            except AttributeError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
        else:
            exitMessage(ec.INVALID_XML, "Invalid XML things")

    def _mul(self, instruction):
        self.args = instruction.args
        if self.args[0].type == 'var' and self.args[1].type in self.SYMB and self.args[2].type in self.SYMB:
            try:
                if self.args[1].type == 'var':
                    frame1, name1 = self.args[1].value.split('@', 1)
                    if frame1 == 'GF':
                        val1 = self.g_frame.get_var_value(name1)
                    elif frame1 == 'TF':
                        val1 = self.t_frame.get_var_value(name1)
                    elif frame1 == 'LF':
                        val1 = self.l_frame[-1].get_var_value(name1)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                elif self.args[1].type == 'int':
                     
                    val1 = int(self.args[1].value)
                else:
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")

                if self.args[2].type == 'var':
                    frame2, name2 = self.args[2].value.split('@', 1)
                    if frame2 == 'GF':
                        val2 = self.g_frame.get_var_value(name2)
                    elif frame2 == 'TF':
                        val2 = self.t_frame.get_var_value(name2)
                    elif frame2 == 'LF':
                        val2 = self.l_frame[-1].get_var_value(name2)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                elif self.args[2].type == 'int': 
                    val2 = int(self.args[2].value)
                else:
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")

                if type(val1) != type(int()) or type(val2) != type(int()):
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                if val1 is None or val2 is None:
                    exitMessage(ec.MISSING_VALUE, "Invalid argument type")        
                    
                frame, name = self.args[0].value.split('@', 1)
                if frame == 'GF':
                    self.g_frame.set_var(name, val1 * val2)
                elif frame == 'TF':
                    self.t_frame.set_var(name, val1 * val2)
                elif frame == 'LF':
                    self.l_frame[-1].set_var(name, val1 * val2)
                else:
                    exitMessage(ec.INVALID_XML, "Invalid frame")
            except IndexError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
            except AttributeError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
        else:
            exitMessage(ec.INVALID_XML, "Invalid XML things")
            
    def _idiv(self, instruction):
        self.args = instruction.args
        if self.args[0].type == 'var' and self.args[1].type in self.SYMB and self.args[2].type in self.SYMB:
            try:
                if self.args[1].type == 'var':
                    frame1, name1 = self.args[1].value.split('@', 1)
                    if frame1 == 'GF':
                        val1 = self.g_frame.get_var_value(name1)
                    elif frame1 == 'TF':
                        val1 = self.t_frame.get_var_value(name1)
                    elif frame1 == 'LF':
                        val1 = self.l_frame[-1].get_var_value(name1)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                elif self.args[1].type == 'int':
                    val1 = int(self.args[1].value)
                else:
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")

                if self.args[2].type == 'var':
                    frame2, name2 = self.args[2].value.split('@', 1)
                    if frame2 == 'GF':
                        val2 = self.g_frame.get_var_value(name2)
                    elif frame2 == 'TF':
                        val2 = self.t_frame.get_var_value(name2)
                    elif frame2 == 'LF':
                        val2 = self.l_frame[-1].get_var_value(name2)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                elif self.args[2].type == 'int': 
                    val2 = int(self.args[2].value)
                else:
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")

                if type(val1) != type(int()) or type(val2) != type(int()):
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                if val1 is None or val2 is None:
                    exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                elif val2 == 0:
                    exitMessage(ec.INVALID_VALUE, "Division by zero")
                 
                frame, name = self.args[0].value.split('@', 1)
                if frame == 'GF':
                    self.g_frame.set_var(name, val1 // val2)
                elif frame == 'TF':
                    self.t_frame.set_var(name, val1 // val2)
                elif frame == 'LF':
                    self.l_frame[-1].set_var(name, val1 // val2)
                else:
                    exitMessage(ec.INVALID_XML, "Invalid frame")
            except IndexError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
            except AttributeError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
        else:
            exitMessage(ec.INVALID_XML, "Invalid XML things")

    def _lt(self, instruction):
        self.args = instruction.args
        if self.args[0].type == 'var' and self.args[1].type in self.SYMB and self.args[2].type in self.SYMB:
            try:
                if self.args[1].type == 'var':
                    frame1, name1 = self.args[1].value.split('@', 1)
                    if frame1 == 'GF':
                        val1 = self.g_frame.get_var_value(name1)
                        typ1 = self.g_frame.get_var_type_str(name1)
                    elif frame1 == 'TF':
                        val1 = self.t_frame.get_var_value(name1)
                        typ1 = self.t_frame.get_var_type_str(name1)
                    elif frame1 == 'LF':
                        val1 = self.l_frame[-1].get_var_value(name1)
                        typ1 = self.l_frame[-1].get_var_type_str(name1)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                    if typ1 == 'nil':
                        exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                elif self.args[1].type == 'int':
                    val1 = int(self.args[1].value)
                    typ1 = self.args[1].type
                elif self.args[1].type in ['bool', 'string']:
                    val1 = self.args[1].value
                    typ1 = self.args[1].type
                else:
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                
                if self.args[2].type == 'var':
                    frame2, name2 = self.args[2].value.split('@', 1)
                    if frame2 == 'GF':
                        val2 = self.g_frame.get_var_value(name2)
                        typ2 = self.g_frame.get_var_type_str(name2)
                    elif frame2 == 'TF':
                        val2 = self.t_frame.get_var_value(name2)
                        typ2 = self.t_frame.get_var_type_str(name2)
                    elif frame2 == 'LF':
                        val2 = self.l_frame[-1].get_var_value(name2)
                        typ2 = self.l_frame[-1].get_var_type_str(name2)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                    if typ2 == 'nil':
                        exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                elif self.args[2].type == 'int':
                    val2 = int(self.args[2].value)
                    typ2 = self.args[2].type
                elif self.args[2].type in ['bool', 'string']:
                    val2 = self.args[2].value
                    typ2 = self.args[2].type
                else:
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")

                if val1 is None or val2 is None:
                    if val1 is None:
                        val1=''
                    if val2 is None:
                        val2=''
                elif typ1 != typ2:
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")

                if val1 < val2:
                    val = 'true'
                else:
                    val = 'false'

                frame, name = self.args[0].value.split('@', 1)
                if frame == 'GF':
                    self.g_frame.set_var(name, val)
                elif frame == 'TF':
                    self.t_frame.set_var(name, val)
                elif frame == 'LF':
                    self.l_frame[-1].set_var(name, val)
                else:
                    exitMessage(ec.INVALID_XML, "Invalid frame")


            except IndexError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
            except AttributeError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
            except TypeError:
                exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
        else:
            exitMessage(ec.INVALID_XML, "Invalid XML things")

    def _gt(self, instruction):
        self.args = instruction.args
        if self.args[0].type == 'var' and self.args[1].type in self.SYMB and self.args[2].type in self.SYMB:
            try:
                if self.args[1].type == 'var':
                    frame1, name1 = self.args[1].value.split('@', 1)
                    if frame1 == 'GF':
                        val1 = self.g_frame.get_var_value(name1)
                        typ1 = self.g_frame.get_var_type_str(name1)
                    elif frame1 == 'TF':
                        val1 = self.t_frame.get_var_value(name1)
                        typ1 = self.t_frame.get_var_type_str(name1)
                    elif frame1 == 'LF':
                        val1 = self.l_frame[-1].get_var_value(name1)
                        typ1 = self.l_frame[-1].get_var_type_str(name1)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                    if typ1 == 'nil':
                        exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                elif self.args[1].type == 'int':
                    val1 = int(self.args[1].value)
                    typ1 = self.args[1].type
                elif self.args[1].type in ['bool', 'string']:
                    val1 = self.args[1].value
                    typ1 = self.args[1].type
                else:
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                
                if self.args[2].type == 'var':
                    frame2, name2 = self.args[2].value.split('@', 1)
                    if frame2 == 'GF':
                        val2 = self.g_frame.get_var_value(name2)
                        typ2 = self.g_frame.get_var_type_str(name2)
                    elif frame2 == 'TF':
                        val2 = self.t_frame.get_var_value(name2)
                        typ2 = self.t_frame.get_var_type_str(name2)
                    elif frame2 == 'LF':
                        val2 = self.l_frame[-1].get_var_value(name2)
                        typ2 = self.l_frame[-1].get_var_type_str(name2)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                    if typ2 == 'nil':
                        exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                elif self.args[2].type == 'int':
                    val2 = int(self.args[2].value)
                    typ2 = self.args[2].type
                elif self.args[2].type in ['bool', 'string']:
                    val2 = self.args[2].value
                    typ2 = self.args[2].type
                else:
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")

                if val1 is None or val2 is None:
                    if val1 is None:
                        val1=''
                    if val2 is None:
                        val2=''
                elif typ1 != typ2:
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")

                if val1 > val2:
                    val = 'true'
                else:
                    val = 'false'

                frame, name = self.args[0].value.split('@', 1)
                if frame == 'GF':
                    self.g_frame.set_var(name, val)
                elif frame == 'TF':
                    self.t_frame.set_var(name, val)
                elif frame == 'LF':
                    self.l_frame[-1].set_var(name, val)
                else:
                    exitMessage(ec.INVALID_XML, "Invalid frame")


            except IndexError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
            except AttributeError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
            except TypeError:
                exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
        else:
            exitMessage(ec.INVALID_XML, "Invalid XML things")

    def _eq(self, instruction):
        self.args = instruction.args
        if self.args[0].type == 'var' and self.args[1].type in self.SYMB and self.args[2].type in self.SYMB:
            try:
                if self.args[1].type == 'var':
                    frame1, name1 = self.args[1].value.split('@', 1)
                    if frame1 == 'GF':
                        val1 = self.g_frame.get_var_value(name1)
                        typ1 = self.g_frame.get_var_type_str(name1)
                    elif frame1 == 'TF':
                        val1 = self.t_frame.get_var_value(name1)
                        typ1 = self.t_frame.get_var_type_str(name1)
                    elif frame1 == 'LF':
                        val1 = self.l_frame[-1].get_var_value(name1)
                        typ1 = self.l_frame[-1].get_var_type_str(name1)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                elif self.args[1].type == 'int':
                    val1 = int(self.args[1].value)
                    typ1 = self.args[1].type
                else:
                    val1 = self.args[1].value
                    typ1 = self.args[1].type
                
                if self.args[2].type == 'var':
                    frame2, name2 = self.args[2].value.split('@', 1)
                    if frame2 == 'GF':
                        val2 = self.g_frame.get_var_value(name2)
                        typ2 = self.g_frame.get_var_type_str(name2)
                    elif frame2 == 'TF':
                        val2 = self.t_frame.get_var_value(name2)
                        typ2 = self.t_frame.get_var_type_str(name2)
                    elif frame2 == 'LF':
                        val2 = self.l_frame[-1].get_var_value(name2)
                        typ2 = self.l_frame[-1].get_var_type_str(name2)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                elif self.args[2].type == 'int':
                    val2 = int(self.args[2].value)
                    typ2 = self.args[2].type
                else:
                    val2 = self.args[2].value
                    typ2 = self.args[2].type
                if val1 is None or val2 is None:
                    if val1 is None:
                        val1=''
                    if val2 is None:
                        val2=''
                elif typ1 in ['string', 'bool', 'int'] and typ2 in ['string', 'bool', 'int'] and typ1 != typ2:
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")

                if val1 == val2:
                    val = 'true'
                else:
                    val = 'false'

                frame, name = self.args[0].value.split('@', 1)
                if frame == 'GF':
                    self.g_frame.set_var(name, val)
                elif frame == 'TF':
                    self.t_frame.set_var(name, val)
                elif frame == 'LF':
                    self.l_frame[-1].set_var(name, val)
                else:
                    exitMessage(ec.INVALID_XML, "Invalid frame")


            except IndexError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
            except AttributeError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
            except TypeError:
                exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
        else:
            exitMessage(ec.INVALID_XML, "Invalid XML things")

    def _and(self, instruction):
        self.args = instruction.args
        if self.args[0].type == 'var' and self.args[1].type in self.SYMB and self.args[2].type in self.SYMB:
            try:
                if self.args[1].type == 'var':
                    frame1, name1 = self.args[1].value.split('@', 1)
                    if frame1 == 'GF':
                        val1 = self.g_frame.get_var_value(name1)
                        if val1 is None:
                            exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                        if self.g_frame.get_var_type_str(name1) != 'bool':
                            exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                    elif frame1 == 'TF':
                        val1 = self.t_frame.get_var_value(name1)
                        if val1 is None:
                            exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                        if self.t_frame.get_var_type_str(name1) != 'bool':
                            exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                    elif frame1 == 'LF':
                        val1 = self.l_frame[-1].get_var_value(name1)
                        if val1 is None:
                            exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                        if self.l_frame[-1].get_var_type_str(name1) != 'bool':
                            exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                elif self.args[1].type == 'bool':
                    val1 = self.args[1].value
                else:
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")

                if self.args[2].type == 'var':
                    frame2, name2 = self.args[2].value.split('@', 1)
                    if frame2 == 'GF':
                        val2 = self.g_frame.get_var_value(name2)
                        if val2 is None:
                            exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                        if self.g_frame.get_var_type_str(name2) != 'bool':
                            exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                    elif frame2 == 'TF':
                        val2 = self.t_frame.get_var_value(name2)
                        if val2 is None:
                            exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                        if self.t_frame.get_var_type_str(name2) != 'bool':
                            exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                    elif frame2 == 'LF':
                        val2 = self.l_frame[-1].get_var_value(name2)
                        if val2 is None:
                            exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                        if self.l_frame[-1].get_var_type_str(name2) != 'bool':
                            exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                elif self.args[2].type == 'bool':
                    val2 = self.args[2].value
                else:
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")

                if val1 is None or val2 is None:
                    exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                if val1 == 'true' and val2 == 'true':
                    val = 'true'
                else:
                    val = 'false'
                
                frame, name = self.args[0].value.split('@', 1)
                if frame == 'GF':
                    self.g_frame.set_var(name, val)
                elif frame == 'TF':
                    self.t_frame.set_var(name, val)
                elif frame == 'LF':
                    self.l_frame[-1].set_var(name, val)
                else:
                    exitMessage(ec.INVALID_XML, "Invalid frame")
            except IndexError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
            except AttributeError:
                exitMessage(ec.INVALID_FRAME, "Invaslid frame")
        else:
            exitMessage(ec.INVALID_XML, "Invalid XML things")

    def _or(self, instruction):
        self.args = instruction.args
        if self.args[0].type == 'var' and self.args[1].type in self.SYMB and self.args[2].type in self.SYMB:
            try:
                if self.args[1].type == 'var':
                    frame1, name1 = self.args[1].value.split('@', 1)
                    if frame1 == 'GF':
                        val1 = self.g_frame.get_var_value(name1)
                        if val1 is None:
                            exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                        if self.g_frame.get_var_type_str(name1) != 'bool':
                            exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                    elif frame1 == 'TF':
                        val1 = self.t_frame.get_var_value(name1)
                        if val1 is None:
                            exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                        if self.t_frame.get_var_type_str(name1) != 'bool':
                            exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                    elif frame1 == 'LF':
                        val1 = self.l_frame[-1].get_var_value(name1)
                        if val1 is None:
                            exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                        if self.l_frame[-1].get_var_type_str(name1) != 'bool':
                            exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                elif self.args[1].type == 'bool':
                    val1 = self.args[1].value
                else:
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")

                if self.args[2].type == 'var':
                    frame2, name2 = self.args[2].value.split('@', 1)
                    if frame2 == 'GF':
                        val2 = self.g_frame.get_var_value(name2)
                        if val2 is None:
                            exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                        if self.g_frame.get_var_type_str(name2) != 'bool':
                            exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                    elif frame2 == 'TF':
                        val2 = self.t_frame.get_var_value(name2)
                        if val2 is None:
                            exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                        if self.t_frame.get_var_type_str(name2) != 'bool':
                            exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                    elif frame2 == 'LF':
                        val2 = self.l_frame[-1].get_var_value(name2)
                        if val2 is None:
                            exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                        if self.l_frame[-1].get_var_type_str(name2) != 'bool':
                            exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                elif self.args[2].type == 'bool':
                    val2 = self.args[2].value
                else:
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")

                if val1 is None or val2 is None:
                    exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                if val1 == 'true' or val2 == 'true':
                    val = 'true'
                else:
                    val = 'false'
                
                frame, name = self.args[0].value.split('@', 1)
                if frame == 'GF':
                    self.g_frame.set_var(name, val)
                elif frame == 'TF':
                    self.t_frame.set_var(name, val)
                elif frame == 'LF':
                    self.l_frame[-1].set_var(name, val)
                else:
                    exitMessage(ec.INVALID_XML, "Invalid frame")
            except IndexError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
            except AttributeError:
                exitMessage(ec.INVALID_FRAME, "Invaslid frame")
        else:
            exitMessage(ec.INVALID_XML, "Invalid XML things")

    def _not(self, instruction):
        self.args = instruction.args
        if self.args[0].type == 'var' and self.args[1].type in self.SYMB:
            try:
                if self.args[1].type == 'var':
                    frame1, name1 = self.args[1].value.split('@', 1)
                    if frame1 == 'GF':
                        val1 = self.g_frame.get_var_value(name1)
                        if val1 is None:
                            exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                        if self.g_frame.get_var_type_str(name1) != 'bool':
                            exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                    elif frame1 == 'TF':
                        val1 = self.t_frame.get_var_value(name1)
                        if val1 is None:
                            exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                        if self.t_frame.get_var_type_str(name1) != 'bool':
                            exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                    elif frame1 == 'LF':
                        val1 = self.l_frame[-1].get_var_value(name1)
                        if val1 is None:
                            exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                        if self.l_frame[-1].get_var_type_str(name1) != 'bool':
                            exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                elif self.args[1].type == 'bool':
                    val1 = self.args[1].value
                else:
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")

                if val1 is None:
                    exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                if val1.lower() not in ['true', 'false']:
                    exitMessage(ec.INVALID_VALUE, "Invalid value")
                if val1.lower() == 'true':
                    val1 = 'false'
                else:
                    val1 = 'true'
                
                frame, name = self.args[0].value.split('@', 1)
                if frame == 'GF':
                    self.g_frame.set_var(name, val1)
                elif frame == 'TF':
                    self.t_frame.set_var(name, val1)
                elif frame == 'LF':
                    self.l_frame[-1].set_var(name, val1)
                else:
                    exitMessage(ec.INVALID_XML, "Invalid frame")
            except IndexError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
            except AttributeError:
                exitMessage(ec.INVALID_FRAME, "Invaslid frame")
        else:
            exitMessage(ec.INVALID_XML, "Invalid XML things")

    def _int2char(self, instruction):
        self.args = instruction.args
        if self.args[0].type == 'var' and self.args[1].type in self.SYMB:
            try:
                if self.args[1].type == 'var':
                    frame1, name1 = self.args[1].value.split('@', 1)
                    if frame1 == 'GF':
                        val1 = self.g_frame.get_var_value(name1)
                        if val1 is None:
                            exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                        if self.g_frame.get_var_type_str(name1) != 'int':
                            exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argsdasdasdsaument type")
                    elif frame1 == 'TF':
                        val1 = self.t_frame.get_var_value(name1)
                        if val1 is None:
                            exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                        if self.t_frame.get_var_type_str(name1) != 'int':
                            exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argumeaddfgjnt type")
                    elif frame1 == 'LF':
                        val1 = self.l_frame[-1].get_var_value(name1)
                        if val1 is None:
                            exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                        if self.l_frame[-1].get_var_type_str(name1) != 'int':
                            exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid arg345345ument type")
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                elif self.args[1].type == 'int':
                    val1 = self.args[1].value
                else:
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argumesdsnt type")

                if val1 is None:
                    exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                try:
                    val1 = int(val1)
                except ValueError:
                    exitMessage(ec.INVALID_VALUE, "Invalid value")
                if val1 < 0 or val1 > 1114111:
                    exitMessage(ec.INVALID_STRING, "Invalid value")
                val1 = chr(val1)
                
                frame, name = self.args[0].value.split('@', 1)
                if frame == 'GF':
                    self.g_frame.set_var(name, val1)
                elif frame == 'TF':
                    self.t_frame.set_var(name, val1)
                elif frame == 'LF':
                    self.l_frame[-1].set_var(name, val1)
                else:
                    exitMessage(ec.INVALID_XML, "Invalid frame")
            except IndexError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
            except AttributeError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
        else:
            exitMessage(ec.INVALID_XML, "Invalid XML things")



    def _stri2int(self, instruction):
        self.args = instruction.args
        if self.args[0].type == 'var' and self.args[1].type in self.SYMB and self.args[2].type in self.SYMB:
            try:
                if self.args[1].type == 'var':
                    frame1, name1 = self.args[1].value.split('@', 1)
                    if frame1 == 'GF':
                        val1 = self.g_frame.get_var_value(name1)
                        if val1 is None:
                            exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                        if self.g_frame.get_var_type_str(name1) != 'string':
                            exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                    elif frame1 == 'TF':
                        val1 = self.t_frame.get_var_value(name1)
                        if val1 is None:
                            exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                        if self.t_frame.get_var_type_str(name1) != 'string':
                            exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                    elif frame1 == 'LF':
                        val1 = self.l_frame[-1].get_var_value(name1)
                        if val1 is None:
                            exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                        if self.l_frame[-1].get_var_type_str(name1) != 'string':
                            exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                elif self.args[1].type == 'string':
                    val1 = self.args[1].value
                else:
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")

                if val1 is None:
                    exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                if self.args[2].type == 'var':
                    frame2, name2 = self.args[2].value.split('@', 1)
                    if frame2 == 'GF':
                        val2 = self.g_frame.get_var_value(name2)
                        if val2 is None:
                            exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                        if self.g_frame.get_var_type_str(name2) != 'int':
                            exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                    elif frame2 == 'TF':
                        val2 = self.t_frame.get_var_value(name2)
                        if val2 is None:
                            exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                        if self.t_frame.get_var_type_str(name2) != 'int':
                            exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                    elif frame2 == 'LF':
                        val2 = self.l_frame[-1].get_var_value(name2)
                        if val2 is None:
                            exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                        if self.l_frame[-1].get_var_type_str(name2) != 'int':
                            exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                elif self.args[2].type == 'int':
                    val2 = self.args[2].value
                else:
                    exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")

                if val2 is None:
                    exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                try:
                    val2 = int(val2)
                except ValueError:
                    exitMessage(ec.INVALID_VALUE, "Invalid value")
                if val2 < 0 or val2 > len(val1)-1:
                    exitMessage(ec.INVALID_STRING, "Invalid string index")
                val1 = val1[val2]
                val1 = ord(val1)

                frame, name = self.args[0].value.split('@', 1)
                if frame == 'GF':
                    self.g_frame.set_var(name, val1)
                elif frame == 'TF':
                    self.t_frame.set_var(name, val1)
                elif frame == 'LF':
                    self.l_frame[-1].set_var(name, val1)
                else:
                    exitMessage(ec.INVALID_XML, "Invalid frame")
            except IndexError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
            except AttributeError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
        else:
            exitMessage(ec.INVALID_XML, "Invalid XML things")

    def _read(self, instruction, inputfile):
        self.args = instruction.args
        val = inputfile.readline()
        if val == '\n':
            val = ''
        elif val == '':
            val = 'nil'
            typ = 'nil'
        else:
            val = val.strip()
        if self.args[0].type == 'var' and self.args[1].type == 'type':
            if val == 'nil' and typ == 'nil':
                pass
            elif self.args[1].value == 'int':
                try:
                    val = int(val)
                    typ = 'int'
                except ValueError:
                    val = 'nil'
                    typ = 'nil'
            elif self.args[1].value == 'bool':
                if val.lower() != 'true':
                    val = 'false'
                else:
                    val = 'true'
                typ = 'bool'
            elif self.args[1].value == 'string':
                typ = 'string'
            else:
                exitMessage(ec.INVALID_XML, "Invalid XML things")

            try:
                frame, name = self.args[0].value.split('@', 1)
                if frame == 'GF':
                    self.g_frame.set_var_type(name, val, typ)
                elif frame == 'TF':
                    self.t_frame.set_var_type(name, val, typ)
                elif frame == 'LF':
                    self.l_frame[-1].set_var_type(name, val, typ)
                else:
                    exitMessage(ec.INVALID_XML, "Invalid frame")
            except IndexError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
            except AttributeError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
        else:
            exitMessage(ec.INVALID_XML, "Invalid XML things")

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
            elif self.args[0].type == Nil() or self.args[0].type == 'nil' or self.args[0].type == type(None):    
                print("", end='')
            else:
                print(self.args[0].value, end='')
        
        else:
            exitMessage(ec.INVALID_XML, "Invalid XML things")


    def _concat(self, instruction):
        self.args = instruction.args
        if self.args[0].type == 'var' and self.args[1].type in self.SYMB and self.args[2].type in self.SYMB:
            if self.args[1].type == 'var':
                try:
                    frame, name = self.args[1].value.split('@', 1)
                    if frame == 'GF':
                        val1 = self.g_frame.get_var_value(name)
                        typ = self.g_frame.get_var_type_str(name)
                    elif frame == 'TF':
                        val1 = self.t_frame.get_var_value(name)
                        typ = self.t_frame.get_var_type_str(name)
                    elif frame == 'LF':
                        val1 = self.l_frame[-1].get_var_value(name)
                        typ = self.l_frame[-1].get_var_type_str(name)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                    if typ != 'string':
                        exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                except IndexError:
                    exitMessage(ec.INVALID_FRAME, "Invalid frame")
                except AttributeError:
                    exitMessage(ec.INVALID_FRAME, "Invalid frame")
            elif self.args[1].type == 'string':
                val1 = self.args[1].value
            else:
                exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
            
            if self.args[2].type == 'var':
                try:
                    frame, name = self.args[2].value.split('@', 1)
                    if frame == 'GF':
                        val2 = self.g_frame.get_var_value(name)
                        typ = self.g_frame.get_var_type_str(name)
                    elif frame == 'TF':
                        val2 = self.t_frame.get_var_value(name)
                        typ = self.t_frame.get_var_type_str(name)
                    elif frame == 'LF':
                        val2 = self.l_frame[-1].get_var_value(name)
                        typ = self.l_frame[-1].get_var_type_str(name)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                    if typ != 'string':
                        exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                except IndexError:
                    exitMessage(ec.INVALID_FRAME, "Invalid frame")
                except AttributeError:
                    exitMessage(ec.INVALID_FRAME, "Invalid frame")
            elif self.args[2].type == 'string':
                val2 = self.args[2].value
            else:
                exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")

            if val1 == None:
                val1 = ''
            if val2 == None:
                val2 = ''

            try:
                frame, name = self.args[0].value.split('@', 1)
                if frame == 'GF':
                    self.g_frame.set_var_type(name, val1+val2, 'string')
                elif frame == 'TF':
                    self.t_frame.set_var_type(name, val1+val2, 'string')
                elif frame == 'LF':
                    self.l_frame[-1].set_var_type(name, val1+val2, 'string')
                else:
                    exitMessage(ec.INVALID_XML, "Invalid frame")
            except IndexError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
            except AttributeError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
        else:
            exitMessage(ec.INVALID_XML, "Invalid XML things")

    def _strlen(self, instruction):
        self.args = instruction.args
        if self.args[0].type == 'var' and self.args[1].type in self.SYMB:
            if self.args[1].type == 'var':
                try:
                    frame, name = self.args[1].value.split('@', 1)
                    if frame == 'GF':
                        val = self.g_frame.get_var_value(name)
                        typ = self.g_frame.get_var_type_str(name)
                    elif frame == 'TF':
                        val = self.t_frame.get_var_value(name)
                        typ = self.t_frame.get_var_type_str(name)
                    elif frame == 'LF':
                        val = self.l_frame[-1].get_var_value(name)
                        typ = self.l_frame[-1].get_var_type_str(name)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                    if typ != 'string':
                        exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                except IndexError:
                    exitMessage(ec.INVALID_FRAME, "Invalid frame")
                except AttributeError:
                    exitMessage(ec.INVALID_FRAME, "Invalid frame")
            elif self.args[1].type == 'string':
                val = self.args[1].value
                if val == None:
                    val = ''
            else:
                exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
            try:
                frame, name = self.args[0].value.split('@', 1)
                if frame == 'GF':
                    self.g_frame.set_var_type(name, len(val), 'int')
                elif frame == 'TF':
                    self.t_frame.set_var_type(name, len(val), 'int')
                elif frame == 'LF':
                    self.l_frame[-1].set_var_type(name, len(val), 'int')
                else:
                    exitMessage(ec.INVALID_XML, "Invalid frame")
            except IndexError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
            except AttributeError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
        pass

    def _getchar(self, instruction):
        self.args = instruction.args
        if self.args[0].type == 'var' and self.args[1].type in self.SYMB and self.args[2].type in self.SYMB:
            if self.args[1].type == 'var':
                try:
                    frame, name = self.args[1].value.split('@', 1)
                    if frame == 'GF':
                        val1 = self.g_frame.get_var_value(name)
                        typ = self.g_frame.get_var_type_str(name)
                    elif frame == 'TF':
                        val1 = self.t_frame.get_var_value(name)
                        typ = self.t_frame.get_var_type_str(name)
                    elif frame == 'LF':
                        val1 = self.l_frame[-1].get_var_value(name)
                        typ = self.l_frame[-1].get_var_type_str(name)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                    if typ != 'string':
                        exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                except IndexError:
                    exitMessage(ec.INVALID_FRAME, "Invalid frame")
                except AttributeError:
                    exitMessage(ec.INVALID_FRAME, "Invalid frame")
            elif self.args[1].type == 'string':
                val1 = self.args[1].value
            else:
                exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
            if self.args[2].type == 'var':
                try:
                    frame, name = self.args[2].value.split('@', 1)
                    if frame == 'GF':
                        val2 = self.g_frame.get_var_value(name)
                        typ = self.g_frame.get_var_type_str(name)
                    elif frame == 'TF':
                        val2 = self.t_frame.get_var_value(name)
                        typ = self.t_frame.get_var_type_str(name)
                    elif frame == 'LF':
                        val2 = self.l_frame[-1].get_var_value(name)
                        typ = self.l_frame[-1].get_var_type_str(name)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                    if typ == None:
                        exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                    elif typ != 'int':
                        exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                except IndexError:
                    exitMessage(ec.INVALID_FRAME, "Invalid frame")
                except AttributeError:
                    exitMessage(ec.INVALID_FRAME, "Invalid frame")
            elif self.args[2].type == 'int':
                if self.args[2].value == None:
                    exitMessage(ec.INVALID_STRING, "Invalid frame")
                val2 = int(self.args[2].value)
            else:
                exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
            if val2 < 0 or val2 >= len(val1):
                exitMessage(ec.INVALID_STRING, "Invalid index of string")
            try:
                frame, name = self.args[0].value.split('@', 1)
                if frame == 'GF':
                    self.g_frame.set_var_type(name, val1[val2], 'string')
                elif frame == 'TF':
                    self.t_frame.set_var_type(name, val1[val2], 'string')
                elif frame == 'LF':
                    self.l_frame[-1].set_var_type(name, val1[val2], 'string')
                else:
                    exitMessage(ec.INVALID_XML, "Invalid frame")
            except IndexError:
                exitMessage(ec.INVALID_FRAME, "Insdsdvalid frame")
            except AttributeError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
        else:
            exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")



    def _setchar(self, instruction):
        self.args = instruction.args
        if self.args[0].type == 'var' and self.args[1].type in self.SYMB and self.args[2].type in self.SYMB:
            if self.args[1].type == 'var':
                try:
                    frame, name = self.args[1].value.split('@', 1)
                    if frame == 'GF':
                        val1 = self.g_frame.get_var_value(name)
                        typ = self.g_frame.get_var_type_str(name)
                    elif frame == 'TF':
                        val1 = self.t_frame.get_var_value(name)
                        typ = self.t_frame.get_var_type_str(name)
                    elif frame == 'LF':
                        val1 = self.l_frame[-1].get_var_value(name)
                        typ = self.l_frame[-1].get_var_type_str(name)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                    if typ == type(None):
                        exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                    elif typ != 'int':
                        exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                except IndexError:
                    exitMessage(ec.INVALID_FRAME, "Invalid frame")
                except AttributeError:
                    exitMessage(ec.INVALID_FRAME, "Invalid frame")
            elif self.args[1].type == 'int':
                if self.args[1].value == None:
                    exitMessage(ec.INVALID_STRING, "Invalid argument value")
                elif int(self.args[1].value) < 0:
                    exitMessage(ec.INVALID_STRING, "Invalid argument value")
                val1 = int(self.args[1].value)
            else:
                exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")

            if self.args[2].type == 'var':
                try:
                    frame, name = self.args[2].value.split('@', 1)
                    if frame == 'GF':
                        val2 = self.g_frame.get_var_value(name)
                        typ = self.g_frame.get_var_type_str(name)
                    elif frame == 'TF':
                        val2 = self.t_frame.get_var_value(name)
                        typ = self.t_frame.get_var_type_str(name)
                    elif frame == 'LF':
                        val2 = self.l_frame[-1].get_var_value(name)
                        typ = self.l_frame[-1].get_var_type_str(name)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                    if typ != 'string':
                        exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                except IndexError:
                    exitMessage(ec.INVALID_FRAME, "Invalid frame")
                except AttributeError:
                    exitMessage(ec.INVALID_FRAME, "Invalid frame")
            elif self.args[2].type == 'string':
                val2 = self.args[2].value
                if val2 == None:
                    exitMessage(ec.INVALID_STRING, "Invalid string")
            else:
                exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
            if len(val2) >= 1:
                val2 = val2[0]
            else:
                exitMessage(ec.INVALID_STRING, "Invalid string")
            
            try:
                frame, name = self.args[0].value.split('@', 1)
                if frame == 'GF':
                    typ = self.g_frame.get_var_type_str(name)
                    if typ == type(None):
                        exitMessage(ec.MISSING_VALUE, "Invalid argument type")
                    elif typ != 'string':
                        exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                    str = self.g_frame.get_var_value(name)
                    if len(str) > val1:
                        self.g_frame.set_var(name, str[:val1] + val2 + str[val1+1:])
                    else:
                        exitMessage(ec.INVALID_STRING, "Invalid string")
                elif frame == 'TF':
                    typ = self.t_frame.get_var_type_str(name)
                    if typ != 'string':
                        exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                    str = self.t_frame.get_var_value(name)
                    if len(str) > val1:
                        self.t_frame.set_var(name, str[:val1] + val2 + str[val1+1:])
                    else:
                        exitMessage(ec.INVALID_STRING, "Invalid string")
                elif frame == 'LF':
                    typ = self.l_frame[-1].get_var_type_str(name)
                    if typ != 'string':
                        exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
                    str = self.l_frame[-1].get_var_value(name)
                    if len(str) > val1:
                        self.l_frame[-1].set_var(name, str[:val1] + val2 + str[val1+1:])
                    else:
                        exitMessage(ec.INVALID_STRING, "Invalid string")
                else:
                    exitMessage(ec.INVALID_XML, "Invalid frame")
            except IndexError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
            except AttributeError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
        else:
            exitMessage(ec.INVALID_VARIABLE, "Invalid argument type") 

    def _type(self, instruction):
        self.args = instruction.args
        if self.args[0].type == 'var' and self.args[1].type in self.SYMB:
            try:
                frame, name = self.args[0].value.split('@', 1)
                if self.args[1].type == 'var': # var var
                    frame2, name2 = self.args[1].value.split('@', 1)
                    if frame2 == 'GF':
                        typ = self.g_frame.get_var_type_str(name2)
                    elif frame2 == 'TF':
                        typ = self.t_frame.get_var_type_str(name2)
                    elif frame2 == 'LF':
                        typ = self.l_frame[-1].get_var_type_str(name2)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")

                else:           # var (int, bool, string, nil)
                    typ = self.args[1].type

                if frame == 'GF':
                    self.g_frame.set_var_type(name, typ, 'string')
                elif frame == 'TF':
                    self.t_frame.set_var_type(name, typ, 'string')
                elif frame == 'LF':
                    self.l_frame[-1].set_var_type(name, typ, 'string')
                else:
                    exitMessage(ec.INVALID_XML, "Invalid frame")
            except IndexError:
                exitMessage(ec.INVALID_FRAME, "Invalid frameERROR")
            except AttributeError:
                exitMessage(ec.INVALID_FRAME, "Invalid frameERROR")
        else:
            exitMessage(ec.INVALID_XML, "Invalid XML things")

    def _label(self, instruction):
        self.args = instruction.args
        if self.args[0].type == 'label':
            pass
        else:
            exitMessage(ec.INVALID_XML, "Invalid XML things")

    def _jump(self, instruction):
        self.args = instruction.args
        try:
            self.instruction_pointer = self.labels[self.args[0].value] - 1
        except KeyError:
            exitMessage(ec.SEMANTIC_ERROR, "Invalid lasddsbel")

    def _jumpifeq(self, instruction):
        self.args = instruction.args
        if self.args[0].type == 'label' and self.args[1].type in self.SYMB and self.args[2].type in self.SYMB:
            try:
                if self.args[1].type == 'var': # var var
                    frame, name = self.args[1].value.split('@', 1)
                    if frame == 'GF':
                        val1 = self.g_frame.get_var_value(name)
                        typ1 = self.g_frame.get_var_type_str(name)
                    elif frame == 'TF':
                        val1 = self.t_frame.get_var_value(name)
                        typ1 = self.t_frame.get_var_type_str(name)
                    elif frame == 'LF':
                        val1 = self.l_frame[-1].get_var_value(name)
                        typ1 = self.l_frame[-1].get_var_type_str(name)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                else:           # var (int, bool, string, nil)
                    typ1 = self.args[1].type
                    if typ1 == 'bool':
                        val1 = self.args[1].value.lower()
                    elif typ1 == 'int':
                        val1 = int(self.args[1].value)
                    else:
                        val1 = self.args[1].value


                if self.args[2].type == 'var': # var var
                    frame, name = self.args[2].value.split('@', 1)
                    if frame == 'GF':
                        val2 = self.g_frame.get_var_value(name)
                        typ2 = self.g_frame.get_var_type_str(name)
                    elif frame == 'TF':
                        val2 = self.t_frame.get_var_value(name)
                        typ2 = self.t_frame.get_var_type_str(name)
                    elif frame == 'LF':
                        val2 = self.l_frame[-1].get_var_value(name)
                        typ2 = self.l_frame[-1].get_var_type_str(name)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                else:           # var (int, bool, string, nil)
                    typ2 = self.args[2].type
                    if typ2 == 'bool':
                        val2 = self.args[2].value.lower()
                    elif typ2 == 'int':
                        val2 = int(self.args[2].value)
                    else:
                        val2 = self.args[2].value
            except IndexError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
            except AttributeError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
            else:
            
                if typ1 != typ2:
                    if typ1 != 'nil' and typ2 != 'nil':
                        exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")

                if self.args[0].value not in self.labels:
                    exitMessage(ec.SEMANTIC_ERROR, "Invalid label")

                if val1 == val2:
                    try:
                        self.instruction_pointer = self.labels[self.args[0].value] - 1
                    except KeyError:
                        exitMessage(ec.SEMANTIC_ERROR, "Missing label")
        else:
            exitMessage(ec.INVALID_XML, "Invalid XML things")


    def _jumpifneq(self, instruction):
        self.args = instruction.args
        if self.args[0].type == 'label' and self.args[1].type in self.SYMB and self.args[2].type in self.SYMB:
            try:
                if self.args[1].type == 'var': # var var
                    frame, name = self.args[1].value.split('@', 1)
                    if frame == 'GF':
                        val1 = self.g_frame.get_var_value(name)
                        typ1 = self.g_frame.get_var_type_str(name)
                    elif frame == 'TF':
                        val1 = self.t_frame.get_var_value(name)
                        typ1 = self.t_frame.get_var_type_str(name)
                    elif frame == 'LF':
                        val1 = self.l_frame[-1].get_var_value(name)
                        typ1 = self.l_frame[-1].get_var_type_str(name)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                else:           # var (int, bool, string, nil)
                    typ1 = self.args[1].type
                    if typ1 == 'bool':
                        val1 = self.args[1].value.lower()
                    elif typ1 == 'int':
                        val1 = int(self.args[1].value)
                    else:
                        val1 = self.args[1].value


                if self.args[2].type == 'var': # var var
                    frame, name = self.args[2].value.split('@', 1)
                    if frame == 'GF':
                        val2 = self.g_frame.get_var_value(name)
                        typ2 = self.g_frame.get_var_type_str(name)
                    elif frame == 'TF':
                        val2 = self.t_frame.get_var_value(name)
                        typ2 = self.t_frame.get_var_type_str(name)
                    elif frame == 'LF':
                        val2 = self.l_frame[-1].get_var_value(name)
                        typ2 = self.l_frame[-1].get_var_type_str(name)
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")
                else:           # var (int, bool, string, nil)
                    typ2 = self.args[2].type
                    if typ2 == 'bool':
                        val2 = self.args[2].value.lower()
                    elif typ2 == 'int':
                        val2 = int(self.args[2].value)
                    else:
                        val2 = self.args[2].value
            except IndexError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
            except AttributeError:
                exitMessage(ec.INVALID_FRAME, "Invalid frame")
            else:
                if typ1 != typ2:
                    if typ1 != 'nil' and typ2 != 'nil':
                        exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")

                if self.args[0].value not in self.labels:
                    exitMessage(ec.SEMANTIC_ERROR, "Missing label")

                if val1 != val2:
                    try:
                        self.instruction_pointer = self.labels[self.args[0].value] - 1
                    except KeyError:
                        exitMessage(ec.SEMANTIC_ERROR, "Missing label")
        else:
            exitMessage(ec.INVALID_XML, "Invalid XML things")

    def _exit(self, instruction):
        self.args = instruction.args
        if self.args[0].type in self.SYMB:
            if self.args[0].type == 'var':
                try:
                    frame, name = self.args[0].value.split('@', 1)
                    if frame == 'GF':
                        if self.g_frame.get_var_type(name) == type(int()) or self.g_frame.get_var_type(name) == type(None):
                            exitMessage(self.g_frame.get_var_value(name), "EXIT")
                    elif frame == 'TF':
                        if self.t_frame.get_var_type(name) == type(int()) or self.t_frame.get_var_type(name) == type(None):
                            exitMessage(self.t_frame.get_var_value(name), "EXIT")
                    elif frame == 'LF':
                        if self.l_frame[-1].get_var_type(name) == type(int()) or self.l_frame[-1].get_var_type(name) == type(None):
                            exitMessage(self.l_frame[-1].get_var_value(name), "EXIT")
                    else:
                        exitMessage(ec.INVALID_XML, "Invalid frame")

                except IndexError:
                    exitMessage(ec.INVALID_FRAME, "Invalid frame")
                except AttributeError:
                    exitMessage(ec.INVALID_FRAME, "Invalid frame")
                    
            elif self.args[0].type == 'int':
                exitMessage(self.args[0].value, "EXIT")
            
            exitMessage(ec.INVALID_OPERAND_TYPE, "Invalid argument type")
        else:
            exitMessage(ec.INVALID_XML, "Invalid XML things")
            

    def _dprint(self, instruction):
        # print(instruction.opcode)
        pass

    def _break(self, instruction):
        # print(instruction.opcode)
        pass
