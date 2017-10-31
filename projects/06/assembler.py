import sys

COMP = {
    '0': '0101010',
    '1': '0111111',
    '-1': '0111010',
    'D': '0001100',
    'A': '0110000',
    '!D': '0001101',
    '!A': '0110001',
    '-D': '0001111',
    '-A': '0110011',
    'D+1': '0011111',
    'A+1': '0110111',
    'D-1': '0001110',
    'A-1': '0110010',
    'D+A': '0000010',
    'D-A': '0010011',
    'A-D': '0000111',
    'D&A': '0000000',
    'D|A': '0010101',
    'M': '1110000',
    '!M': '1110001',
    '-M': '1110011',
    'M+1': '1110111',
    'M-1': '1110010',
    'D+M': '1000010',
    'D-M': '1010011',
    'M-D': '1000111',
    'D&M': '1000000',
    'D|M': '1010101',
}
DEST = {
    'null': '000',
    'M': '001',
    'D': '010',
    'MD': '011',
    'A': '100',
    'AM': '101',
    'AD': '110',
    'AMD': '111',
}
JUMP = {
    'null': '000',
    'JGT': '001',
    'JEQ': '010',
    'JGE': '011',
    'JLT': '100',
    'JNE': '101',
    'JLE': '110',
    'JMP': '111',
}


class Parser(object):
    def __init__(self, data):
        self.commands = []
        for line in data:
            line = line.strip()
            if not line:
                continue
            if line[0] == '/':
                continue
            self.commands.append(self.remove_trailing_comments(line))

    def remove_trailing_comments(self, line):
        if "/" in line:
            line = line.split("/", 1)[0]
        return line.strip()


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


class Translator(object):
    def handle_C_instruction(self, line):
        # parse it into dest=comp;jump
        # return string concatenated by lookups
        translated_string = '111'
        if '=' in line:
            split_line = line.split('=')
            dest_lookup = split_line[0]
            comp_lookup = split_line[1]
            jump_lookup = 'null'
        elif ';' in line:
            split_line = line.split(';')
            comp_lookup = split_line[0]
            jump_lookup = split_line[1]
            dest_lookup = 'null'
        binary_comp = COMP[comp_lookup]
        binary_dest = DEST[dest_lookup]
        binary_jump = JUMP[jump_lookup]
        return translated_string + binary_comp + binary_dest + binary_jump


class Main(object):
    def __init__(self, f):
        self.asm_file = f
        self.table = SymbolTable()
        self.data = self.read_file()
        self.parser = Parser(self.data)
        self.commands = self.parser.commands
        self.translator = Translator()
        self.filename = self.asm_file.split(".")[0]

    def read_file(self):
        with open(self.asm_file) as f:
            data = f.readlines()
        return data

    def write_file(self, output_lines):
        with open('%sassembled.hack' % self.filename, 'w') as output_file:
            for line in output_lines:
                output_file.write(line + '\n')

    def assemble(self):
        self.first_pass()
        output_lines = self.second_pass()
        self.write_file(output_lines)

    def first_pass(self):
        program_line = 0
        for line in self.commands:
            # if we have encountered a label pseudocommand
            # check if it is in the table, if not assign it to value of next program line
            # don't increment program counter because this shouldn't count as a program line
            if line[0] == '(':
                if not self.table.contains(line[1:-1]):
                    self.table.add_entry(line[1:-1], program_line)
                continue
            # if none of these conditions are hit, keep incrementing program line
            program_line += 1

    def second_pass(self):
        translated_commands = []
        next_available_RAM = 16
        for line in self.commands:
            if line[0] == '@':
                symbol = line[1:]
                try:
                    # translate directly if @ is referencing a specific value
                    translated_commands.append('{0:016b}'.format(int(symbol)))
                    continue
                except ValueError:
                    pass
                # check if symbol is already in the symbol table and convert value to binary
                if self.table.contains(symbol):
                    translated_commands.append('{0:016b}'.format(self.table.get_address(symbol)))
                # add symbol to symbol table, increment available RAM count, and translate to binary
                else:
                    self.table.add_entry(symbol, next_available_RAM)
                    next_available_RAM += 1
                    translated_commands.append('{0:016b}'.format(self.table.get_address(symbol)))
            elif line[0] == '(':
                continue
            else:
                translated_commands.append(self.translator.handle_C_instruction(line))
        return translated_commands


if __name__ == "__main__":
    try:
        assembler = Main(sys.argv[1])
        assembler.assemble()
    except IndexError as e:
        print "Error: Requires an assembly file as input"
