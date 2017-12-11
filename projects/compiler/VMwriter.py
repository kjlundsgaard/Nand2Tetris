kind_lookup = {
    'arg': 'argument',
    'var': 'local',
    'field': 'this',
    'static': 'static',
    'constant': 'constant',
    'temp': 'temp',
    'pointer': 'pointer',
    'that': 'that',
}

binary_operation_table = {
    '+': 'add',
    '-': 'sub',
    '>': 'gt',
    '<': 'lt',
    '=': 'eq',
    '|': 'or',
    '&': 'and',
    '/': 'call Math.divide 2',
    '*': 'call Math.multiply 2',
}

unary_operation_table = {
    '-': 'neg',
    '~': 'not',
}


class VMWriter(object):
    def __init__(self):
        self.commands = []

    def write_call(self, method_name, num_args):
        # TODO: probably need to deal with pop pointer 0/setting "this" segment of RAM
        command = 'call {} {}'.format(method_name, num_args)
        self.commands.append(command)

    def write_push(self, kind, index):
        command = 'push {} {}'.format(kind_lookup[kind], index)
        self.commands.append(command)

    def write_pop(self, kind, index):
        command = 'pop {} {}'.format(kind_lookup[kind], index)
        self.commands.append(command)

    def write_arithmetic(self, operation, unary=False):
        op = unary_operation_table[operation] if unary else binary_operation_table[operation]
        command = '{}'.format(op)
        self.commands.append(command)

    def write_return(self):
        command = 'return'
        self.commands.append(command)

    def write_function(self, f_name, num_locals):
        command = 'function {} {}'.format(f_name, num_locals)
        self.commands.append(command)

    def write_label(self, label):
        command = 'label {}'.format(label)
        self.commands.append(command)

    def write_goto(self, label):
        command = 'goto {}'.format(label)
        self.commands.append(command)

    def write_if(self, label):
        command = 'if-goto {}'.format(label)
        self.commands.append(command)

    def create_file(self, filename):
        with open('{}TEST.vm'.format(filename), 'w') as f:
            f.write('\n'.join(self.commands))
