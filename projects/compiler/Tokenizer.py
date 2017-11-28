

class Tokenizer(object):
    """
    Takes single or multiple .jack files and tokenizes the files
    """
    def __init__(self, file_contents):
        self.contents = self.clean(file_contents)

    def has_more_tokens(self):
        """returns true if there are still tokens to be parsed"""
        return len(self.contents) > 0

    def advance(self):
        """gets next token from the input"""
        curr_token = self.contents[0]
        self.contents = self.contents[1:]
        return curr_token

    def tokenize(self):
        pass

    def clean(self, file_contents):
        """removes whitespace and comments"""
        result = []
        for line in file_contents:
            line = line.split("//")[0]
            line = line.split("/*")[0]
            line = line.strip()
            if not line:
                continue
            result.append(line)
        return result
