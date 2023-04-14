import re

class Instruction:
    INSTRUCTIONS = {
        'MOVE': ['var', 'symb'],
        'CREATEFRAME': [],
        'PUSHFRAME': [],
        'POPFRAME': [],
        'DEFVAR': ['var'],
        'CALL': ['label'],
        'RETURN': [],
        'PUSHS': ['symb'],
        'POPS': ['var'],
        'ADD': ['var', 'symb', 'symb'],
        'SUB': ['var', 'symb', 'symb'],
        'MUL': ['var', 'symb', 'symb'],
        'IDIV': ['var', 'symb', 'symb'],
        'LT': ['var', 'symb', 'symb'],
        'GT': ['var', 'symb', 'symb'],
        'EQ': ['var', 'symb', 'symb'],
        'AND': ['var', 'symb', 'symb'],
        'OR': ['var', 'symb', 'symb'],
        'NOT': ['var', 'symb'],
        'INT2CHAR': ['var', 'symb'],
        'STRI2INT': ['var', 'symb', 'symb'],
        'READ': ['var', 'type'],
        'WRITE': ['symb'],
        'CONCAT': ['var', 'symb', 'symb'],
        'STRLEN': ['var', 'symb'],
        'GETCHAR': ['var', 'symb', 'symb'],
        'SETCHAR': ['var', 'symb', 'symb'],
        'TYPE': ['var', 'symb'],
        'LABEL': ['label'],
        'JUMP': ['label'],
        'JUMPIFEQ': ['label', 'symb', 'symb'],
        'JUMPIFNEQ': ['label', 'symb', 'symb'],
        'EXIT': ['symb'],
        'DPRINT': ['symb'],
        'BREAK': []
    }

    def __init__(self, ins):
        self.order = ins[0]
        self.opcode = ins[1]
        self.args = []
        for i in range(2, len(ins), 2):
            self.args.append(Argument(ins[i], ins[i+1]))
    
    def get_order(self):
        return self.order
    
    def get_opcode(self):
        return self.opcode
    
    def get_args(self):
        return self.args
    
    def len_args(self):
        return len(self.args)
    
    
class Argument(Instruction):
    def __init__(self, arg_type, arg_value):
        self.name = None
        self.type = arg_type
        self.value = arg_value
        if arg_type == 'string':
            self.value = re.sub(r'\\([0-9]{3})', lambda x: chr(int(x.group(1))), str(arg_value))

    def get_arg(self):
        return self.name, self.type, self.value
    
    
