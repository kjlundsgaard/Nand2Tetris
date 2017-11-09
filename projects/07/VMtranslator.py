import sys
import os


def read_file(filename):
    """opens the input file"""
    with open(filename) as f:
        data = f.readlines()
    return data


class Parser():
    """parses each VM command into lexical elements"""
    def __init__(self, filenames):
        self.all_file_data = []
        for f in filenames:
            file_data = read_file(f)
            self.all_file_data.extend(file_data)
        self.commands = (line for line in self.all_file_data)

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

    def __init__(self, basename):
        self.input_filename = basename
        self.mapping = {
            'local': 'LCL',
            'argument': 'ARG',
            'this': 'THIS',
            'that': 'THAT',
            'temp': '5',
            'pointer': '3',
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
            jump_command = "J"+asm_command.upper()
            self.append_command("""//{cmd}
                @R14
                M=-1 //-1 is 0xfffffff which is true
                @SP
                D=M
                A=D-1
                D=M
                A=A-1
                //D is zero if x and y are equal
                D=M-D
                //decrement stack point
                @SP
                M=M-1
                //jump if values are equal, greaterthan, or lessthan
                @{filename}.jmp{ctr}
                D;{jump_command}
                //if we're here, the jump condition failed, so set R14 to false
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
                self.append_command("""//push constant {value}
                @{value}
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1""".format(value=value))
            if segment in set(['temp', 'pointer']):
                self.append_command("""//push {segment} {index}
                @{seg_map}
                D=A
                @{index}
                A=D+A
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1""".format(segment=segment, index=value, seg_map=self.mapping[segment]))
            if segment in set(['local', 'argument', 'this', 'that']):
                self.append_command("""//push {segment} {index}
                @{seg_map}
                D=M
                @{index}
                A=D+A
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1""".format(segment=segment, index=value, seg_map=self.mapping[segment]))
            if segment == 'static':
                self.append_command("""//push static {index}
                @{filename}.{index}
                D=M
                @SP
                A=M
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
                A=M-1
                D=M
                @{filename}.{index}
                M=D
                @SP
                M=M-1""".format(index=value, filename=self.input_filename))
            if segment in set(['temp', 'pointer']):
                self.append_command("""//pop {segment} {index}
                @{seg_map}
                D=A
                @{index}
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
                M=M-1""".format(segment=segment, index=value, seg_map=self.mapping[segment]))
            if segment in set(['local', 'argument', 'this', 'that']):
                self.append_command("""//pop {segment} {index}
                @{seg_map}
                D=M
                @{index}
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
                M=M-1""".format(segment=segment, index=value, seg_map=self.mapping[segment]))

    def append_command(self, asm_commands):
        """push new set of asm commands into list"""
        self.commands_list.append(asm_commands)


class Main():
    """Drives the process of opening, translating, and writing
    VMcode to assembly
    """

    def __init__(self, vm_file):
        self.filename = vm_file
        self.basename = os.path.splitext(os.path.basename(vm_file))[0]
        self.writer = CodeWriter(self.basename)
        self.directory = os.path.dirname(vm_file)
        self.suffix = '.asm'
        self.abspath = os.path.abspath(self.filename)

    def translate(self):
        if self.filename == '.' or self.filename == '..':
            all_filenames = self.get_files_from_directory(self.abspath)
        elif self.directory and not self.filename.endswith('.vm'):
            all_filenames = self.get_files_from_directory(self.directory)
        else:
            all_filenames = [self.filename]

        parser = Parser(all_filenames)
        command = parser.advance()
        while command:
            # could be returning None if whitespace - returns tuples of empty strings?
            parsed_elements = parser.parse(command)
            if parsed_elements:
                self.writer.compose(parsed_elements)
            command = parser.advance()
        self.write_file()

    def write_file(self):
        """writes and saves output assembly file"""
        # put an infinite loop at the end of the program
        if self.directory:
            # this means a path to a file was passed in
            if self.filename.endswith('.vm'):
                output_filename = '{directory}/{filename}{suffix}'.format(
                    directory=self.directory,
                    filename=self.basename,
                    suffix=self.suffix
                )
            else:
                # this means a directory was passed in rather than a file
                output_filename = '{directory}/{filename}{suffix}'.format(
                    directory=self.directory,
                    filename=os.path.abspath(self.directory).split('/')[-1],
                    suffix=self.suffix
                )

        else:
            # handle case of if . or .. is passed
            if not self.filename.endswith('.vm'):
                output_filename = '{directory}/{filename}{suffix}'.format(
                    directory=self.filename,
                    filename=os.path.abspath(self.abspath).split('/')[-1],
                    suffix=self.suffix
                )
            else:
                # this means we are already in the directory of the file
                output_filename = '{filename}{suffix}'.format(
                    filename=self.basename,
                    suffix=self.suffix
                )
        self.writer.commands_list.append("""
            (END)
            @END
            0;JMP   //FOREVER LOOP""")
        with open('%s' % output_filename, 'w') as output_file:
            print('writing to {}'.format(output_filename))
            output_file.write('\n'.join(self.writer.commands_list))

    def get_files_from_directory(self, folder):
        """takes in a single directory and translates all *.vm files in that path"""
        return ['{}/{}'.format(folder, each) for each in os.listdir(folder) if each.endswith('.vm')]

if __name__ == "__main__":
    try:
        translator = Main(sys.argv[1])
    except IndexError as e:
        print "Error: Requires a vmcommand file as input"
    translator.translate()
