from errorCodes import ErrorCodes as ec, exitMessage

class Nil:
    def __init__(self):
        pass
    
    def __name__(self):
        return 'nil'


class Frame:
    def __init__(self):
        self.frame = {}

    try:
        def get_frame(self):
            try:
                return self.frame
            except:
                exitMessage(ec.INVALID_FRAME, "Frame doesn't exist")

        def def_var(self, var):
            if var not in self.frame.keys():
                self.frame[var] = (None, type(None))
            else:
                exitMessage(ec.SEMANTIC_ERROR, "Variable already exists")
                

        def set_var(self, var, value):
            if var in self.frame.keys():
                if type(value) == Nil() or value == 'nil':
                    self.frame[var] = (value, Nil())
                elif type(value) == type(bool()) or value == 'true' or value == 'false':
                    self.frame[var] = (value, type(bool()))
                else:
                    self.frame[var] = (value, type(value))
            else:
                exitMessage(ec.INVALID_VARIABLE, "Variable doesn't exist")

        def set_var_type(self, var, value, typ):
            if var in self.frame.keys():
                if typ == 'int':
                    self.frame[var] = (value, type(int()))
                elif typ == 'bool':
                    self.frame[var] = (value, type(bool()))
                elif typ == 'string':
                    self.frame[var] = (value, type(str()))
                elif typ == 'nil':
                    self.frame[var] = (value, Nil())
                else:
                    self.frame[var] = (value, typ)
            else:
                exitMessage(ec.INVALID_VARIABLE, "Variable doesn't exist")
            
        def get_var(self, var):
            if var in self.frame.keys():
                return self.frame[var]
            else:
                exitMessage(ec.INVALID_VARIABLE, "Variable doesn't exist")
        
        def get_var_value(self, var):
            if var in self.frame.keys():
                return self.frame[var][0]
            else:
                exitMessage(ec.INVALID_VARIABLE, "Variable doesn't exist")
        
        def get_var_type(self, var):
            if var in self.frame.keys():
                return self.frame[var][1]
            else:
                # print("~~~~~~~")
                # print(self.frame.keys(),var)
                exitMessage(ec.INVALID_VARIABLE, "Variable doesn't exist")

        def get_var_type_str(self, var):
            if var in self.frame.keys():
                if self.frame[var][1].__name__ == 'str':
                    return 'string'
                elif type(self.frame[var][1]) == type(Nil()):
                    return 'nil'
                else:
                    return self.frame[var][1].__name__
            else:
                # print("~~~~~~~")
                # print(self.frame.keys(),var)
                exitMessage(ec.INVALID_VARIABLE, "Variable doesn't exist")


        def write_frame(self):
            print(self.frame)

        def write_var(self, var):
            if self.get_var_type(var) != type(None):
                print(self.get_var_value(var), end='')
            else:
                exitMessage(ec.MISSING_VALUE, "Variable doesn't exist")

    except AttributeError:
        exitMessage(ec.INTERNAL_ERROR, "Invalid fasdsdrame")
    
