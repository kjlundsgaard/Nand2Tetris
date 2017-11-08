import sys
import os


def read_file(filename):
    """opens the input file"""
    with open(filename) as f:
        data = f.readlines()
    return data


class Parser():
    """parses each VM command into lexical elements"""
    def __init__(self, filename):
        self.file_data = read_file(filename)
        self.commands = (line for line in self.file_data)

    def advance(self):
        return next(self.commands, None)

    def parse(self, command):
        command_type = ""
        arg_one = ""
        arg_two = ""

        # get rid of whitespace
        command = command.strip()
        if not command:
            return

        # ignore commented lines
        if command[0] == "/":
            return
        # get rid of comments at end of line
        command = command.split("//")[0]
        command = command.strip()

        elements = command.split(" ")
        command_type = self.get_command_type(elements[0])
        if command_type == 'C_ARITHMETIC':
            arg_one = elements[0]
        elif command_type != 'C_RETURN' and command_type != '':
            arg_one = elements[1]
        if command_type in ('C_POP', 'C_PUSH', 'C_FUNCTION', 'C_CALL'):
            arg_two = elements[2]

        return (command_type, arg_one, arg_two)

    def get_command_type(self, command):
        """
        returns constant indicating command type
        C_ARITHMETIC
        C_PUSH
        C_POP
        C_LABEL
        C_GOTO
        C_IF
        C_FUNCTION
        C_RETURN
        C_CALL
        """
        arithmetic_commands = set(['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not'])
        if command in arithmetic_commands:
            return 'C_ARITHMETIC'
        elif command == 'push':
            return 'C_PUSH'
        elif command == 'pop':
            return 'C_POP'
        else:
            return ''


class CodeWriter():
    """writes the assembly code that implements the parsed command"""

    def __init__(self, filename):
        self.input_filename = os.path.splitext(os.path.basename(filename))[0]
        self.mapping = {
            'local': 'LCL',
            'argument': 'ARG',
            'this': 'THIS',
            'that': 'THAT',
            'temp': '5',
        }
        self.jump_ctr = 0
        self.commands_list = []

    def compose(self, commands):
        """determines which type of command to use and passes to corresponding write method"""
        command_type, arg_one, arg_two = commands
        if not command_type:
            return
        if command_type == 'C_ARITHMETIC':
            command = arg_one
            # arg_one will be the arithmetic command we need to translate into assembly
            self.write_arithmetic(command)
        if command_type == 'C_PUSH' or command_type == 'C_POP':
            segment = arg_one
            value = arg_two
            self.write_push_pop(command_type, segment, value)

    def write_arithmetic(self, asm_command):
        """composes arithmetic commands in assembly and passes to write_file"""
        if asm_command == 'add':
            # access memory value of SP - 1 and SP - 2
            self.append_command("""//add
                @SP
                D=M
                A=D-1
                D=M
                A=A-1
                M=D+M
                @SP
                M=M-1""")
        elif asm_command == 'sub':
            # mostly same as add except order of M-D might be wrong????
            self.append_command("""//sub
                @SP
                D=M
                A=D-1
                D=M
                A=A-1
                M=M-D
                @SP
                M=M-1""")
        elif asm_command == 'neg':
            self.append_command("""//neg
                @SP
                D=M
                A=D-1
                M=-M""")
        elif asm_command in set(['eq', 'lt', 'gt']):
            jump_command = "J"+asm_command.to_upper()
            self.append_command("""//{cmd}
                @-1 //-1 is 0xfffffff which is true
                D=A
                @R14
                M=D
                @SP
                D=M
                A=D-1
                D=M
                A=A-1
                //D is zero if x and y are equal
                D=D-M
                //decrement stack point
                @SP
                M=M-1
                //jump if values are equal
                @{filename}.jmp{ctr}
                D;{jump_command}
                //if we're here, x!=y, so set R14 to false
                @R14
                M=0
            ({filename}.jmp{ctr})
                //push R14 onto stack
                @R14
                D=M
                @SP
                A=M-1
                M=D
                """.format(cmd=asm_command, jump_command=jump_command, filename=self.input_filename, ctr=self.jump_ctr))
            self.jump_ctr += 1
        elif asm_command == 'gt':
            pass
        elif asm_command == 'lt':
            pass
        elif asm_command == 'and':
            self.append_command("""//and
                @SP
                D=M
                A=D-1
                D=M
                A=A-1
                M=M&D
                @SP
                M=M-1""")
        elif asm_command == 'or':
            self.append_command("""//or
                @SP
                D=M
                A=D-1
                D=M
                A=A-1
                M=M|D
                @SP
                M=M-1""")
        elif asm_command == 'not':
            self.append_command("""//not
                @SP
                D=M
                A=D-1
                M=!M""")

    def write_push_pop(self, asm_command, segment, value):
        """composes pushpop commands in assembly and passes to write_file"""
        if asm_command == 'C_PUSH':
            if segment == 'constant':
                self.append_command("""//push constant {}
                @{}
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1""".format(value, value))
            if segment in set(['local', 'argument', 'this', 'that', 'temp']):
                self.append_command("""//push {} {}
                @{}
                D=M
                @{}
                A=D+A
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1""".format(segment, value, self.mapping[segment], value))
            if segment == 'static':
                self.append_command("""//push static {index}
                @{filename}.{index}
                D=M
                @SP
                M=D
                @SP
                M=M+1""".format(index=value, filename=self.input_filename))
        if asm_command == 'C_POP':
            if segment == 'constant':
                # raise error
                raise('cannot pop a constant')
            if segment == 'static':
                self.append_command("""//pop static {index}
                @SP
                A=A-1
                D=M
                @{filename}.{index}
                M=D
                @SP
                M=M-1
                """.format(index=value, filename=self.input_filename))
            if segment in set(['local', 'argument', 'this', 'that', 'temp']):
                self.append_command("""//pop {} {}
                @{}
                D=M
                @{}
                D=D+A
                @R13
                M=D
                @SP
                A=M-1
                D=M
                @R13
                A=M
                M=D
                @SP
                M=M-1""".format(segment, value, self.mapping[segment], value))

    def append_command(self, asm_commands):
        """push new set of asm commands into list"""
        self.commands_list.append(asm_commands)


class Main():
    """Drives the process of opening, translating, and writing
    VMcode to assembly
    """

    def __init__(self, vm_file):
        self.filename = vm_file
        self.parser = Parser(self.filename)
        self.writer = CodeWriter('{}.asm'.format(self.filename))
        self.output_filename = vm_file.split('.')[0]

    def translate(self):
        command = self.parser.advance()
        while command:
            # could be returning None if whitespace - returns tuples of empty strings?
            parsed_elements = self.parser.parse(command)
            if parsed_elements:
                self.writer.compose(parsed_elements)
            command = self.parser.advance()
        self.write_file()

    def write_file(self):
        """writes and saves output assembly file"""
        with open('%s.asm' % self.output_filename, 'w') as output_file:
            print('writing to {}.asm'.format(self.output_filename))
            output_file.write('\n'.join(self.writer.commands_list))


if __name__ == "__main__":
    try:
        translator = Main(sys.argv[1])
    except IndexError as e:
        print "Error: Requires a vmcommand file as input"
    translator.translate()
