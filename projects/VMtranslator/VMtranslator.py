import sys
import os
from parser import Parser
from codewriter import CodeWriter


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
        self.write_file(parser)

    def write_file(self, parser):
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
        parser.asm_commands_list.append("""
            (END)
            @END
            0;JMP   //FOREVER LOOP""")
        # import pdb;pdb.set_trace()
        with open('%s' % output_filename, 'w') as output_file:
            print('writing to {}'.format(output_filename))
            output_file.write('\n'.join(parser.asm_commands_list))

    def get_files_from_directory(self, folder):
        """takes in a single directory and translates all *.vm files in that path"""
        return ['{}/{}'.format(folder, each) for each in os.listdir(folder) if each.endswith('.vm')]

if __name__ == "__main__":
    try:
        translator = Main(sys.argv[1])
    except IndexError as e:
        print "Error: Requires a vmcommand file as input"
    translator.translate()
