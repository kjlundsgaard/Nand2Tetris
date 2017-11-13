import os


class CodeWriter():
    """writes the assembly code that implements the parsed command"""

    def __init__(self, input_filename):
        self.input_filename = os.path.splitext(os.path.basename(input_filename))[0]
        self
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
            return self.write_arithmetic(command)
        if command_type == 'C_PUSH' or command_type == 'C_POP':
            segment = arg_one
            value = arg_two
            return self.write_push_pop(command_type, segment, value)

    def write_arithmetic(self, asm_command):
        """composes arithmetic commands in assembly and passes to write_file"""
        if asm_command == 'add':
            # access memory value of SP - 1 and SP - 2
            return ("""//add
                @SP
                D=M
                A=D-1
                D=M
                A=A-1
                M=D+M
                @SP
                M=M-1""")
        elif asm_command == 'sub':
            return ("""//sub
                @SP
                D=M
                A=D-1
                D=M
                A=A-1
                M=M-D
                @SP
                M=M-1""")
        elif asm_command == 'neg':
            return ("""//neg
                @SP
                D=M
                A=D-1
                M=-M""")
        elif asm_command in set(['eq', 'lt', 'gt']):
            jump_command = "J"+asm_command.upper()
            translated_command = ("""//{cmd}
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
            return translated_command
        elif asm_command == 'and':
            return ("""//and
                @SP
                D=M
                A=D-1
                D=M
                A=A-1
                M=M&D
                @SP
                M=M-1""")
        elif asm_command == 'or':
            return ("""//or
                @SP
                D=M
                A=D-1
                D=M
                A=A-1
                M=M|D
                @SP
                M=M-1""")
        elif asm_command == 'not':
            return ("""//not
                @SP
                D=M
                A=D-1
                M=!M""")

    def write_push_pop(self, asm_command, segment, value):
        """composes pushpop commands in assembly and passes to write_file"""
        if asm_command == 'C_PUSH':
            if segment == 'constant':
                return ("""//push constant {value}
                @{value}
                D=A
                @SP
                A=M
                M=D
                @SP
                M=M+1""".format(value=value))
            if segment in set(['temp', 'pointer']):
                return ("""//push {segment} {index}
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
                return ("""//push {segment} {index}
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
                return ("""//push static {index}
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
                return ("""//pop static {index}
                @SP
                A=M-1
                D=M
                @{filename}.{index}
                M=D
                @SP
                M=M-1""".format(index=value, filename=self.input_filename))
            if segment in set(['temp', 'pointer']):
                return ("""//pop {segment} {index}
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
                return ("""//pop {segment} {index}
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
