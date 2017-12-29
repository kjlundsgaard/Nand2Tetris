class SymbolTable(object):
    def __init__(self):
        self.table = {}
        self. initialize_predefined_symbols()

    def initialize_predefined_symbols(self):
        self.add_entry('SP', 0)
        self.add_entry('LCL', 1)
        self.add_entry('ARG', 2)
        self.add_entry('THIS', 3)
        self.add_entry('THAT', 4)
        for i in range(0, 16):
            self.add_entry('R%s' % i, i)
        self.add_entry('SCREEN', 16384)
        self.add_entry('KBD', 24576)

    def add_entry(self, symbol, value):
        self.table[symbol] = value

    def contains(self, symbol):
        if symbol in self.table:
            return True
        else:
            return False

    def get_address(self, symbol):
        return self.table[symbol]
