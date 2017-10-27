import sys

class Parser(object):
    def __init__(self, data):
	self.commands = data
   
    def next_command(self, gen):
	try:
	    return next(gen)
	except StopIteration:
	    return None    
    def unpack(self, data):
	return (line for line in data) 
    
    def parse(self, line):
	print line

class SymbolTable(object):
    def __init__(self):
	self.table = {} 
    
    def initialize_predefined_symbols(self):
	pass

    def add_entry(symbol, value):
	self.table[symbol] = value

    def contains(symbol):
	if symbol in self.table:
	    return True
	else:
	    return False
	
    def get_address(symbol):
	return self.table[symbol]
 
class Translater(object):
    def __init__(self):
	pass

class Main(object):
    def __init__(self, f):
	self.asm_file = f

    def read_file(self):
	with open(self.asm_file) as f:
	    data = f.readlines()	
	return data

    def write_file(self):
	pass
    
    def assemble(self):
	data = self.read_file()
	parser = Parser(data)
	generator = parser.unpack(data)
	next_command = parser.next_command(generator)
	while next_command:
	    parser.parse(next_command)
	    next_command = parser.next_command(generator)
	return

if __name__ == "__main__":
    try:
	assembler = Main(sys.argv[1])
	assembler.assemble()	
    except IndexError as e:
	print "Error: Requires an assembly file as input" 
