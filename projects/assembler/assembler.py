import sys
from symboltable import SymbolTable
from translator import Translator
from parser import Parser


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
