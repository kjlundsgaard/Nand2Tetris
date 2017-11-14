import os


class CodeWriter():
    """writes the assembly code that implements the parsed command"""

    def __init__(self, input_filename):
        self.input_filename = os.path.splitext(os.path.basename(input_filename))[0]
        self.mapping = {
            'local': 'LCL',
            'argument': 'ARG',
            'this': 'THIS',
            'that': 'THAT',
            'temp': '5',
            'pointer': '3',
        }
        self.jump_ctr = 0
        self.rt_ctr = 0
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
        elif command_type == 'C_PUSH' or command_type == 'C_POP':
            segment = arg_one
            value = arg_two
            return self.write_push_pop(command_type, segment, value)
        elif command_type == 'C_LABEL':
            label = arg_one
            return self.write_label(label)
        elif command_type == 'C_GOTO':
            label = arg_one
            return self.write_goto(label)
        elif command_type == 'C_IF':
            label = arg_one
            return self.write_if(label)
        elif command_type == 'C_FUNCTION':
            fn_name = arg_one
            num_locals = arg_two
            return self.write_function(fn_name, num_locals)
        elif command_type == 'C_CALL':
            fn_name = arg_one
            num_args = arg_two
            return self.write_call(fn_name, num_args)
        elif command_type == 'C_RETURN':
            return self.write_return()

    def write_label(self, label):
        """writes assembly code that effects the label command
        assigns a label
        """
        return ("""// label
            ({filename}${label})
        """).format(filename=self.input_filename, label=label)

    def write_goto(self, label):
        """writes assmebly code that effects the goto command
        indiscriminately jumps to the label
        """
        return (""" // goto label
            @{filename}${label}
            0;JEQ
        """).format(filename=self.input_filename, label=label)

    def write_if(self, label):
        """writes assembly that effects the if-goto command
        pops stack pointer value and jumps to label if value is not zero
        """
        return (""" // if-goto label
            @SP
            A=M-1
            D=M
            @SP
            M=M-1
            @{filename}${label}
            D;JNE
        """).format(filename=self.input_filename, label=label)

    def write_function(self, fn_name, num_locals):
        """writes the assembly code that declares a function
        establishes function label and initializes local variables to zero
        """
        return ("""// function {fn_name} {num_locals}
        ({fn_name})
            @{num_locals}
            D=A
            @{fn_name}.END_LOOP
            D;JLE
            ({fn_name}.initloop)
            @SP
            A=M
            M=0
            @SP
            M=M+1
            D=D-1
            @{fn_name}.initloop
            D;JGT
            ({fn_name}.END_LOOP)
        """).format(fn_name=fn_name, num_locals=num_locals)

    def write_call(self, fn_name, num_args):
        """writes assembly code that effects the call command
        saves frame of caller and assigns local variables
        """
        translated_command = ("""// call {fn_name} {num_args}
            //push returnAddress
            @{fn_name}.returnAddress.{rt_ctr}
            D=A
            @SP
            A=M
            M=D
            @SP
            M=M+1
            // push LCL
            @LCL
            D=M
            @SP
            A=M
            M=D
            @SP
            M=M+1
            // push ARG
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
            @{num_args}
            D=D-A
            @ARG
            M=D
            // LCL = SP
            @SP
            D=M
            @LCL
            M=D
            // goto {fn_name}
            @{fn_name}
            0;JMP
        ({fn_name}.returnAddress.{rt_ctr})
        """).format(fn_name=fn_name, num_args=num_args, rt_ctr=self.rt_ctr)
        self.rt_ctr += 1
        return translated_command

    def write_return(self):
        """writes assembly code that effects the return command
        returns value of function return to top of stack and recycles memory
        """
        translated_command = (""" // return
            // frame = LCL
            @LCL
            D=M
            @FRAME
            M=D
            // retAddr = *(frame-5)
            @5
            D=A
            @FRAME
            D=M-D
            A=D
            D=M
            @RET.{rt_ctr}
            M=D
            // *ARG = pop
            @SP
            A=M-1
            D=M
            @ARG
            A=M
            M=D
            // SP = ARG + 1
            @ARG
            D=M+1
            @SP
            M=D
            // THAT = *(frame-1)
            @FRAME
            D=M
            @1
            A=D-A
            D=M
            @THAT
            M=D
            // THIS = *(frame-2)
            @FRAME
            D=M
            @2
            A=D-A
            D=M
            @THIS
            M=D
            // ARG = *(frame-3)
            @FRAME
            D=M
            @3
            A=D-A
            D=M
            @ARG
            M=D
            // LCL = *(frame-4)
            @FRAME
            D=M
            @4
            A=D-A
            D=M
            @LCL
            M=D
            @RET.{rt_ctr}
            A=M
            0;JMP
        """).format(rt_ctr=self.rt_ctr)
        self.rt_ctr += 1
        return translated_command

    def write_arithmetic(self, asm_command):
        """composes arithmetic commands in assembly"""
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
        """composes pushpop commands in assembly"""
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
