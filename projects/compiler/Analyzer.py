import os
import sys
from tokenizer import Tokenizer
from compilationengine import CompilationEngine


class Analyzer(object):
    """
    Operates on a given source that is either a file name of form Xxx.jack
    or a directory name with one or more such files. For each file,
    the analyzer tokenizes the file, creates a .xml file, and uses compilation
    engine to compile the tokenizer input into the output file
    """

    def __init__(self, fordir):
        self.files = self.get_files_from_directory(fordir)

    def get_files_from_directory(self, fordir):
        """takes in a file or single directory and gets all *.jack files in that path"""
        if fordir.endswith('.jack'):
            return [os.path.abspath(fordir)]
        else:
            directory = fordir
            return ['{}'.format(os.path.abspath(os.path.join(directory, each))) for each in os.listdir(fordir) if each.endswith('.jack')]

    def write_tokens(self, tokenizer):
        """writes tokens to xml file"""
        output_file = '{}ktT.xml'.format(tokenizer.filename[:-5])
        with open(output_file, 'w') as f:
            print 'writing tokens to {}'.format(output_file)
            f.write(''.join(tokenizer.token_output))

    def write_syntax_tree(self, compilation_engine):
        """writes parse tree to xml file"""
        output_file = '{}ktCST.xml'.format(compilation_engine.filename[:-5])
        with open(output_file, 'w') as f:
            print 'writing syntax tree to {}'.format(output_file)
            f.write(''.join(compilation_engine.contents))

    def analyze(self):
        """
        uses compilation engine to compile tokenized input
        """
        for f in self.files:
            tokenizer = Tokenizer(f)
            self.write_tokens(tokenizer)
            compilation_engine = CompilationEngine(tokenizer, f)
            compilation_engine.compile()
            self.write_syntax_tree(compilation_engine)


if __name__ == "__main__":
    try:
        compiler = Analyzer(sys.argv[1])
    except IndexError as e:
        print "Error: Requires a .jack file or directory as input"
    compiler.analyze()
