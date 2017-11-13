from codewriter import CodeWriter


def read_file(filename):
    """opens the input file"""
    with open(filename) as f:
        data = f.readlines()
    return data


class Parser():
    """parses each VM command into lexical elements"""
    def __init__(self, filenames):
        self.asm_commands_list = []
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
