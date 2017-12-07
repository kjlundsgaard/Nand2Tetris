class SymbolTable(object):
    def __init__(self):
        self.class_symbols = {}
        self.sub_symbols = {}
        self.static_index = 0
        self.field_index = 0
        self.arg_index = 0
        self.var_index = 0

    def add_class_var(self, tokens):
        kind = tokens[0]
        cl_type = tokens[1]
        for name in tokens[2:]:
            self.add_symbol(self.class_symbols, kind, cl_type, name)

    def add_sub_var(self, kind, cl_type, name):
        self.add_symbol(self.sub_symbols, kind, cl_type, name)

    def add_symbol(self, scope, kind, s_type, name):
        if kind == "static":
            index = self.static_index
            self.static_index += 1
        elif kind == "field":
            index = self.field_index
            self.field_index += 1
        elif kind == "arg":
            index = self.arg_index
            self.arg_index += 1
        elif kind == "var":
            index = self.var_index
            self.var_index += 1
        else:
            raise Exception("{} is not a valid symbol kind.".format(kind))

        scope[name] = {'kind': kind, 'type': s_type, 'index': index}

    def reset_subroutine(self):
        self.arg_index = 0
        self.var_index = 0
        self.sub_symbols = {}
