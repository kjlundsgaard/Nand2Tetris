from codewriter import CodeWriter
import os


def read_file(filename):
    """opens the input file"""
    with open(filename) as f:
        data = f.readlines()
    return data


class Parser():
    """parses each VM command into lexical elements"""
    def __init__(self, filenames):
        self.asm_commands_list = []
        file_basenames = set([os.path.splitext(os.path.basename(f))[0] for f in filenames])
        if 'Sys' in file_basenames:
            self.write_init()
        for f in filenames:
            file_data = (line for line in read_file(f))
            writer = CodeWriter(f)
            command = self.advance(file_data)
            while command:
                parsed_elements = self.parse(command)
                if parsed_elements:
                    self.asm_commands_list.append(writer.compose(parsed_elements))
                command = self.advance(file_data)

    def advance(self, generator):
        return next(generator, None)

    def write_init(self):
        pass
        # self.asm_commands_list.append("""
        #     @256
        #     D=A
        #     @SP
        #     M=D
        #     @Sys.init
        #     0;JMP
        # """)
        self.asm_commands_list.append("""
            @256
            D=A
            @SP
            M=D
            @RET_Sys.init
            D=A
            @SP
            A=M
            M=D
            @SP
            M=M+1
            @LCL
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            @ARG
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            // push THIS
            @THIS
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            // push THAT
            @THAT
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            // ARG = SP - {num_args} - 5
            @SP
            D=M
            @5
            D=D-A
            @ARG
            M=D
            // LCL = SP
            @SP
            D=M
            @LCL
            M=D
            @Sys.init
            0;JMP
            (RET_Sys.init)
        """)

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
        elif command == 'label':
            return 'C_LABEL'
        elif command == 'goto':
            return 'C_GOTO'
        elif command == 'if-goto':
            return 'C_IF'
        elif command == 'function':
            return 'C_FUNCTION'
        elif command == 'call':
            return 'C_CALL'
        elif command == 'return':
            return 'C_RETURN'
        else:
            return ''
