import os
import sys
from Tokenizer import Tokenizer
from CompilationEngine import CompilationEngine


class Analyzer(object):
    """
    Operates on a given source that is either a file name of form Xxx.jack
    or a directory name with one or more such files. For each file,
    the analyzer tokenizes the file, creates a .xml file, and uses compilation
    engine to compile the tokenizer input into the output file
    """

    def __init__(self, fordir):
        self.build_file_contents(fordir)
        self.output_file = self.get_output_file(fordir)
        self.tokenizer = Tokenizer(self.file_contents)
        self.compilation_engine = CompilationEngine()
        self.compiled_lines = []

    def get_output_file(self, fordir):
        """
        creates name of xml output file to be written to
        """
        if fordir.endswith('.jack'):
            return '{}.xml'.format(os.path.abspath(fordir)[:-5])
        else:
            return '{}.xml'.format(os.path.abspath(fordir))

    def build_file_contents(self, fordir):
        """
        determines if a file or directory has been passed in and
        calls appropriate read_file method to build the file_contents attribute
        """
        self.file_contents = []
        if fordir.endswith('.jack'):
            self.file_contents.extend(self.read_file(fordir))
        else:
            files = self.get_files_from_directory(fordir)
            for f in files:
                self.file_contents.extend(self.read_file(f))

    def get_files_from_directory(self, folder):
        """takes in a single directory and gets all *.jack files in that path"""
        return ['{}'.format(os.path.abspath(each)) for each in os.listdir(folder) if each.endswith('.jack')]

    def read_file(self, filename):
        """opens the input file"""
        with open(filename) as f:
            data = f.readlines()
        return data

    def analyze(self):
        """
        uses compilation engine to compile tokenized input
        """
        while self.tokenizer.has_more_tokens():
            line_to_tokenize = self.tokenizer.advance()
            tokens = self.tokenizer.tokenize(line_to_tokenize)
            self.compile(tokens)
        self.write_file(self.compiled_lines)

    def compile(self, tokens):
        """parses the tokens and outputs structured xml output of code"""
        for token in tokens:
            # TODO: actually parse stuff
            self.compiled_lines.append(token)

    def write_file(self, lines):
        """writes to xml file"""
        with open('{}' % self.output_file, 'w') as output_file:
            print('writing to {}'.format(self.output_file))
            output_file.write('\n'.join(lines))


if __name__ == "__main__":
    try:
        compiler = Analyzer(sys.argv[1])
    except IndexError as e:
        print "Error: Requires a .jack file or directory as input"
    # compiler.analyze()
