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
