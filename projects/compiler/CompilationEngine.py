from symboltable import SymbolTable
from VMwriter import VMWriter

ops = set(['+', '-', '*', '/', '&', '|', '<', '>', '='])

unary_ops = set(['-', '~'])

op_translate = {
    '<': '&lt;',
    '>': '&gt;',
    '&': '&amp;'
}


class CompilationEngine(object):
    """
    Compiles tokenized input
    """
    def __init__(self, tokenizer, filename):
        self.filename = filename
        self.tokenizer = tokenizer
        self.VMwriter = VMWriter()
        self.contents = []
        self.indent = 0
        # self.label_index = 0

    def compile(self):
        self.compile_class()
        # print self.VMwriter.commands

    def write_next_token(self, op_replace=None):
        self.tokenizer.advance()
        token_type = self.tokenizer.get_token_type()
        if not op_replace:
            token = self.tokenizer.get_token_value()
        else:
            token = op_replace
        self.contents.append("\t" * self.indent + "<{token_type}> {token} </{token_type}>\n"
            .format(token_type=token_type, token=token))

        return token

    # 'class' className '{' classVarDec* subroutineDec* '}'
    def compile_class(self):
        # create symbol table for class
        self.symbol_table = SymbolTable()
        self.add_opening_tag('class')
        self.increase_indent()
        self.write_next_token()  # 'class'
        self.class_name = self.write_next_token()  # className
        self.write_next_token()  # {
        while self.tokenizer.has_more_tokens():
            if self.tokenizer.look_ahead()[1] in set(['static', 'field']):
                self.compile_class_var_dec()
            elif self.tokenizer.look_ahead()[1] in set(['function', 'constructor', 'method']):
                self.compile_subroutine()
            elif self.tokenizer.look_ahead()[1] == '}':
                self.write_next_token()  # }
        # print self.symbol_table.class_symbols
        self.decrease_indent()
        self.add_closing_tag('class')

    # ('static' | 'field' ) type varName (',' varName)* ';'
    def compile_class_var_dec(self):
        tokens = []
        self.add_opening_tag('classVarDec')
        self.increase_indent()
        while self.tokenizer.look_ahead()[1] != ';':
            tokens.append(self.write_next_token())
        self.symbol_table.add_class_var(tokens)
        self.write_next_token()
        self.decrease_indent()
        self.add_closing_tag('classVarDec')

    # ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
    def compile_subroutine(self):
        self.symbol_table.reset_subroutine()
        # add class to sub_symbols table

        self.add_opening_tag('subroutineDec')
        self.increase_indent()
        f_type = self.write_next_token()  # constructor|function|method
        # if f_type in {'method', 'constructor'}:
        if f_type == 'method':
            self.symbol_table.add_sub_var('arg', self.class_name, 'this')
        self.write_next_token()  # 'void'|type
        f_name = self.write_next_token()  # subroutineName
        self.write_next_token()  # (
        self.compile_param_list()
        self.write_next_token()  # )
        # tokens = { varDec*
        self.write_next_token()  # {
        num_locals = 0
        while self.tokenizer.look_ahead()[1] == 'var':
            # figure out number of vars
            num_locals += self.compile_var_dec()

        self.VMwriter.write_function('{}.{}'.format(self.class_name, f_name), num_locals)
        if f_type == 'method':
            # push this
            self.VMwriter.write_push('arg', 0)
            # store memory address of this obj in this
            self.VMwriter.write_pop('pointer', 0)
        elif f_type == 'constructor':
            # push fields onto stack, allocate that much memory
            num_fields = self.symbol_table.num_field_vars()
            self.VMwriter.write_push('constant', num_fields)
            self.VMwriter.write_call('Memory.alloc', 1)
            self.VMwriter.write_pop('pointer', 0)
        self.compile_subroutine_body()
        self.decrease_indent()
        self.add_closing_tag('subroutineDec')

    # statements '}'
    def compile_subroutine_body(self):
        self.add_opening_tag('subroutineBody')
        self.increase_indent()
        while self.tokenizer.look_ahead()[1] != '}':
                self.compile_statements()
        self.write_next_token()  # }
        self.decrease_indent()
        self.add_closing_tag('subroutineBody')

    # ( (type varName) (',' type varName)*)?
    def compile_param_list(self):
        self.add_opening_tag('parameterList')
        self.increase_indent()
        while self.tokenizer.look_ahead()[1] != ')':
            token = self.tokenizer.look_ahead()
            if token[0] == 'keyword':
                token_type = token[1]
            if token[0] == 'identifier':
                token_name = token[1]
                self.symbol_table.add_sub_var('arg', token_type, token_name)
            self.write_next_token()
        self.decrease_indent()
        self.add_closing_tag('parameterList')

    # 'var' type varName (',' varName)* ';'
    def compile_var_dec(self):
        self.add_opening_tag('varDec')
        self.increase_indent()
        self.write_next_token()  # var
        token_type = self.write_next_token()  # type
        num_vars = 0
        while self.tokenizer.look_ahead()[1] != ';':
            token = self.tokenizer.look_ahead()
            if token[0] == 'identifier':
                num_vars += 1
                token_name = token[1]
                self.symbol_table.add_sub_var('var', token_type, token_name)
            self.write_next_token()
        self.write_next_token()  # ;
        self.decrease_indent()
        self.add_closing_tag('varDec')
        return num_vars

    # statement*
    # letStatement | ifStatement | whileStatement | doStatement | returnStatement
    def compile_statements(self):
        self.add_opening_tag('statements')
        self.increase_indent()
        while self.tokenizer.look_ahead()[1] != '}':
            if self.tokenizer.look_ahead()[1] == 'do':
                self.compile_do()
            elif self.tokenizer.look_ahead()[1] == 'let':
                self.compile_let()
            elif self.tokenizer.look_ahead()[1] == 'while':
                self.compile_while()
            elif self.tokenizer.look_ahead()[1] == 'if':
                self.compile_if()
            elif self.tokenizer.look_ahead()[1] == 'return':
                self.compile_return()
        self.decrease_indent()
        self.add_closing_tag('statements')

    # subroutineCall: subroutineName '(' expressionList ')' | ( className | varName) '.' subroutineName '(' expressionList ')'
    def compile_subroutine_call(self):
        call_name = self.write_next_token()  # subroutineName|className|varName
        # lookup in symbol table call_name
        symbol = self.symbol_table.sub_symbols.get(call_name, None)
        if not symbol:
            symbol = self.symbol_table.class_symbols.get(call_name, None)
        # entering expressionlist
        # subroutine case 2: show(x, y, z) (method)
        if self.tokenizer.look_ahead()[1] == '(':
            self.write_next_token()  # (
            # first push class as "this"
            self.VMwriter.write_push('pointer', 0)
            num_exp = self.compile_expression_list() + 1
            self.write_next_token()  # )
            self.VMwriter.write_call('{}.{}'.format(self.class_name, call_name), num_exp)
        # subroutineCall case 1:
        elif self.tokenizer.look_ahead()[1] == '.':
            self.write_next_token()  # .
            method_name = self.write_next_token()  # subroutineName
            self.write_next_token()  # (
            # game.run()
            if symbol:
                self.VMwriter.write_push(symbol['kind'], symbol['index'])
                call_name = symbol['type']
            # Math.multiply(x, y)
            num_exp = self.compile_expression_list()
            if symbol:
                # this means we're operating on a method
                num_exp += 1
            # writes the VM command that calls the function with number of args
            self.VMwriter.write_call('{}.{}'.format(call_name, method_name), num_exp)
            self.write_next_token()  # )

    # 'do' subroutineCall ';'
    def compile_do(self):
        self.add_opening_tag('doStatement')
        self.increase_indent()
        self.write_next_token()  # do
        self.compile_subroutine_call()  # subroutine call
        # throw away top stack item
        self.VMwriter.write_pop('temp', 0)
        self.write_next_token()  # ;
        self.decrease_indent()
        self.add_closing_tag('doStatement')

    # 'let' varName ('[' expression ']')? '=' expression ';'
    def compile_let(self):
        self.add_opening_tag('letStatement')
        self.increase_indent()
        self.write_next_token()  # let
        token = self.write_next_token()  # varName
        symbol = self.symbol_table.sub_symbols.get(token, None)
        if not symbol:
            symbol = self.symbol_table.class_symbols.get(token, None)
        # [ expression ]
        did_index = False
        if self.tokenizer.look_ahead()[1] == '[':
            # only push if we're indexing array
            self.VMwriter.write_push(symbol['kind'], symbol['index'])
            did_index = True
            self.write_next_token()  # [
            self.compile_expression()  # expression
            self.write_next_token()  # ]
            # add token and index (from compiled expression)
            self.VMwriter.write_arithmetic('+')
        self.write_next_token()  # =
        # write expression and place on stack
        self.compile_expression()
        if did_index:
            self.VMwriter.write_pop('temp', 0)
            self.VMwriter.write_pop('pointer', 1)
            self.VMwriter.write_push('temp', 0)
            self.VMwriter.write_pop('that', 0)
        else:
            self.VMwriter.write_pop(symbol['kind'], symbol['index'])
            # pop symboltable[symbol]
        self.write_next_token()  # ;
        self.decrease_indent()
        self.add_closing_tag('letStatement')

    # 'while' '(' expression ')' '{' statements '}'
    def compile_while(self):
        self.add_opening_tag('whileStatement')
        self.increase_indent()
        self.write_next_token()  # while
        self.VMwriter.write_label('WHILE_COND{}'.format(self.indent))
        self.write_next_token()  # (
        self.compile_expression()
        self.write_next_token()  # )
        self.VMwriter.write_arithmetic('~', unary=True)
        self.VMwriter.write_if('END_WHILE{}'.format(self.indent))
        self.write_next_token()  # {
        while self.tokenizer.look_ahead()[1] != '}':
            self.compile_statements()
        self.write_next_token()  # }
        self.VMwriter.write_goto('WHILE_COND{}'.format(self.indent))
        self.VMwriter.write_label('END_WHILE{}'.format(self.indent))
        self.decrease_indent()
        self.add_closing_tag('whileStatement')

    # 'return' expression? ';'
    def compile_return(self):
        self.add_opening_tag('returnStatement')
        self.increase_indent()
        self.write_next_token()  # return
        # returns nothing
        if self.tokenizer.look_ahead()[1] == ';':
            self.VMwriter.write_push('constant', 0)
        while self.tokenizer.look_ahead()[1] != ';':
            self.compile_expression()
        # write return
        self.VMwriter.write_return()
        self.write_next_token()  # ;
        self.decrease_indent()
        self.add_closing_tag('returnStatement')

    # 'if' '(' expression ')' '{' statements '}' ( 'else' '{' statements '}' )?
    #  if (expression) {s1} else {s2}
    #  if (expression) {s1} ==> not expression; if-goto l1; s1; l1
    def compile_if(self):
        self.add_opening_tag('ifStatement')
        self.increase_indent()
        self.write_next_token()  # if
        self.write_next_token()  # (
        self.compile_expression()
        self.write_next_token()  # )
        # not expression
        self.VMwriter.write_arithmetic('~', unary=True)
        # if-goto l1
        self.VMwriter.write_if('IF_FALSE{}'.format(self.indent))
        # s1
        self.write_next_token()  # {
        self.compile_statements()  # s1
        self.write_next_token()  # }
        # [else]
        # goto end
        self.VMwriter.write_goto('END_OF_IF{}'.format(self.indent))
        self.VMwriter.write_label('IF_FALSE{}'.format(self.indent))

        if self.tokenizer.look_ahead()[1] == 'else':  # l1
            self.write_next_token()  # else
            # write label for else code executions
            self.write_next_token()  # {
            self.compile_statements()  # s2
            self.write_next_token()  # }
        # end
        self.VMwriter.write_label('END_OF_IF{}'.format(self.indent))
        # self.label_index += 1
        self.decrease_indent()
        self.add_closing_tag('ifStatement')

    # term (op term)*
    def compile_expression(self):
        self.add_opening_tag('expression')
        self.increase_indent()
        self.compile_term()  # term
        while self.tokenizer.look_ahead()[1] in ops:
            self.tokenizer.look_ahead()[1]
            # if next_token_value in set(['>', '<', '&']):
            #     self.write_next_token(op_replace=op_translate[next_token_value])  # op
            # elif next_token_value == ',':
            #     break
            # else:
            operation = self.write_next_token()  # op
            self.compile_term()
            self.VMwriter.write_arithmetic(operation)
        self.decrease_indent()
        self.add_closing_tag('expression')

    # integerConstant | stringConstant | keywordConstant | varName |
    # varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
    def compile_term(self):
        self.add_opening_tag('term')
        self.increase_indent()
        next_token = self.tokenizer.look_ahead()
        if next_token[1] in unary_ops:
            operation = self.write_next_token()  # unaryOp
            self.compile_term()  # term
            self.VMwriter.write_arithmetic(operation, unary=True)
        elif next_token[1] == '(':
            self.write_next_token()  # (
            self.compile_expression()  # expression
            self.write_next_token()  # )
        else:  # some sort of identifier is present first
            # subroutineCall
            if self.tokenizer.tokens[1][1] in {'.', '('}:
                self.compile_subroutine_call()
            # varname|intconstant|stringconstant|keywordconstant
            else:
                token = self.write_next_token()  # write identifer
                token_type = self.tokenizer.get_token_type()
                symbol = self.symbol_table.sub_symbols.get(token, None)
                if not symbol:
                    symbol = self.symbol_table.class_symbols.get(token, None)
                # varName ([expression])?
                if symbol and token != 'this':
                    # evaluating a term, so needs to be on stack
                    self.VMwriter.write_push(symbol['kind'], symbol['index'])
                    # [ expression ]
                    if self.tokenizer.look_ahead()[1] == '[':
                        self.write_next_token()  # [
                        self.compile_expression()  # expression
                        self.write_next_token()  # ]
                        # add token and index (from compiled expression)
                        self.VMwriter.write_arithmetic('+')
                        # pop pointer 1
                        self.VMwriter.write_pop('pointer', 1)
                        self.VMwriter.write_push('that', 0)
                # intConstant, stringConstant, keywordConstant
                elif token_type == 'integerConstant':
                    self.VMwriter.write_push('constant', token)
                elif token_type == 'stringConstant':
                    self.VMwriter.write_push('constant', len(token))
                    self.VMwriter.write_call('String.new', 1)
                    for char in token:
                        self.VMwriter.write_push('constant', ord(char))
                        self.VMwriter.write_call('String.appendChar', 2)
                elif token_type == 'keyword':
                    if token in {'null', 'false'}:
                        self.VMwriter.write_push('constant', 0)
                    elif token == 'true':
                        self.VMwriter.write_push('constant', 0)
                        self.VMwriter.write_arithmetic('~', unary=True)
                    elif token == 'this':
                        self.VMwriter.write_push('pointer', 0)
                    else:
                        raise Exception('Unkown keyword!')
                else:
                    raise Exception('Unkown term!')
        self.decrease_indent()
        self.add_closing_tag('term')

    # (expression (',' expression)* )?
    def compile_expression_list(self):
        self.add_opening_tag('expressionList')
        self.increase_indent()
        num_exp = 0
        while self.tokenizer.look_ahead()[1] not in set([')', ']']):
            if self.tokenizer.look_ahead()[1] == ',':
                self.write_next_token()  # ,
            else:
                self.compile_expression()
                num_exp += 1
        self.decrease_indent()
        self.add_closing_tag('expressionList')
        return num_exp

    def increase_indent(self):
        self.indent += 1

    def decrease_indent(self):
        self.indent -= 1

    def write_token(self, token):
        token_str = token + "\n"
        self.contents.append(token_str)

    def add_opening_tag(self, tagname):
        tag_str = "\t" * self.indent + "<{}>\n".format(tagname)
        self.contents.append(tag_str)

    def add_closing_tag(self, tagname):
        tag_str = "\t" * self.indent + "</{}>\n".format(tagname)
        self.contents.append(tag_str)
