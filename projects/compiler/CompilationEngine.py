
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
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.contents = []
        self.indent = 0

    def compile(self):
        self.add_opening_tag("tokens")
        self.compile_class()
        self.add_closing_tokens_tag("tokens")

    def write_next_token(self, op_replace=None):
        self.tokenizer.advance()
        token_type = self.tokenizer.get_token_type()
        if not op_replace:
            token = self.tokenizer.get_token_value()
        else:
            token = op_replace
        self.contents.append("\t" * self.indent + "<{token_type}>{token}</{token_type}>\n"
            .format(token_type=token_type, token=token))

    # 'class' className '{' classVarDec* subroutineDec* '}'
    def compile_class(self):
        self.increase_indent()
        self.add_opening_tag('class')
        self.increase_indent()
        self.write_next_token()  # 'class'
        self.write_next_token()  # className
        self.write_next_token()  # {
        while self.tokenizer.has_more_tokens():
            if self.tokenizer.look_ahead()[1] in set(['static', 'field']):
                self.compile_class_var_dec()
            if self.tokenizer.look_ahead()[1] in set(['function', 'constructor', 'method']):
                self.compile_subroutine()

        self.decrease_indent()
        self.add_closing_tag('class')

    # ('static' | 'field' ) type varName (',' varName)* ';'
    def compile_class_var_dec(self):
        self.add_opening_tag('classVarDec')
        self.increase_indent()
        while self.tokenizer.get_token_value() != ';':
            self.write_next_token()
        self.write_next_token()
        self.decrease_indent()
        self.add_closing_tag('classVarDec')

    # ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
    def compile_subroutine(self):
        self.add_opening_tag('subroutineDec')
        self.increase_indent()
        while self.tokenizer.look_ahead()[1] != '(':
            self.write_next_token()  # constructor|function|method void|type subroutineName
        self.write_next_token()  # (
        self.compile_param_list()
        self.write_next_token()  # )
        self.compile_subroutine_body()
        self.decrease_indent()
        self.add_closing_tag('subroutineDec')

    # '{' varDec* statements '}'
    def compile_subroutine_body(self):
        # import pdb;pdb.set_trace()
        self.add_opening_tag('subroutineBody')
        self.increase_indent()
        self.write_next_token()  # {
        while self.tokenizer.look_ahead()[1] != '}':
            if self.tokenizer.get_token_value() == 'var':
                self.compile_var_dec()
            else:
                self.compile_statements()
        self.write_next_token()  # }
        self.decrease_indent()
        self.add_closing_tag('subroutineBody')

    # ( (type varName) (',' type varName)*)?
    def compile_param_list(self):
        self.add_opening_tag('paramList')
        self.increase_indent()
        while self.tokenizer.look_ahead()[1] != ')':
            self.write_next_token()
        self.decrease_indent()
        self.add_closing_tag('paramList')

    # 'var' type varName (',' varName)* ';'
    def compile_var_dec(self):
        self.add_opening_tag('varDec')
        self.increase_indent()
        while self.tokenizer.get_token_value() != ';':
            self.write_next_token()
        self.write_next_token()  # ;
        self.decrease_indent()
        self.add_closing_tag('varDec')

    # statement*
    # letStatement | ifStatement | whileStatement | doStatement | returnStatement
    def compile_statements(self):
        self.add_opening_tag('statements')
        self.increase_indent()
        if self.tokenizer.get_token_value() == 'do':
            self.compile_do()
        elif self.tokenizer.get_token_value() == 'let':
            self.compile_let()
        elif self.tokenizer.get_token_value() == 'while':
            self.compile_while()
        elif self.tokenizer.get_token_value() == 'return':
            self.compile_return()
        elif self.tokenizer.get_token_value() == 'if':
            self.compile_if()
        self.decrease_indent()
        self.add_closing_tag('statements')

    # 'do' subroutineCall ';'
    # subroutineCall: subroutineName '(' expressionList ')' | ( className | varName) '.' subroutineName '(' expressionList ')'
    def compile_do(self):
        self.add_opening_tag('doStatement')
        self.increase_indent()
        while self.tokenizer.look_ahead()[1] != ';':
            # entering expressionlist
            if self.tokenizer.get_token_value() == '(':
                self.write_next_token()  # (
                self.compile_expression_list()
            else:
                self.write_next_token()
        self.write_next_token()  # ;
        self.decrease_indent()
        self.add_closing_tag('doStatement')

    # 'let' varName ('[' expression ']')? '=' expression ';'
    def compile_let(self):
        self.add_opening_tag('letStatement')
        self.increase_indent()
        self.write_next_token()  # let
        self.write_next_token()  # varName
        if self.tokenizer.look_ahead()[1] == '[':
            self.write_next_token()  # [
            self.compile_expression()
            self. write_next_token  # ]
        self.write_next_token()  # =
        self.compile_expression()
        # write expression
        self.write_next_token()  # ;
        self.decrease_indent()
        self.add_closing_tag('letStatement')

    # 'while' '(' expression ')' '{' statements '}'
    def compile_while(self):
        self.add_opening_tag('whileStatement')
        self.increase_indent()
        self.write_next_token()  # while
        self.write_next_token()  # (
        self.compile_expression()
        self. write_next_token()  # )
        self.write_next_token()  # {
        self.compile_statements()
        self.write_next_token()  # }
        self.decrease_indent()
        self.add_closing_tag('whileStatement')

    # 'return' expression? ';'
    def compile_return(self):
        self.add_opening_tag('returnStatement')
        self.increase_indent()
        self.write_next_token()  # return
        while self.tokenizer.look_ahead()[1] != ';':
            self.write_expression()
        self.write_next_token()  # ;
        self.decrease_indent()
        self.add_closing_tag('returnStatement')

    # 'if' '(' expression ')' '{' statements '}' ( 'else' '{' statements '}' )?
    def compile_if(self):
        self.add_opening_tag('ifStatement')
        self.increase_indent()
        self.write_next_token()  # if
        self.write_next_token()  # (
        self.write_expression()
        self.write_next_token()  # )
        self.write_next_token()  # {
        self.write_statements()
        self.write_next_token()  # }
        if self.tokenizer.look_ahead()[1] == 'else':
            self.write_next_token()  # else
            self.write_next_token()  # {
            self.write_statements()
            self.write_next_token()  # }
        self.decrease_indent()
        self.add_closing_tag('ifStatement')

    # term (op term)*
    def compile_expression(self):
        self.add_opening_tag('expression')
        self.increase_indent()
        self.compile_term()  # term
        while self.tokenizer.look_ahead()[1] in ops:
            next_token_value = self.tokenizer.look_ahead()[1]
            if next_token_value in set(['>', '<', '&']):
                self.write_next_token(op_replace=op_translate[next_token_value])  # op
            else:
                self.write_next_token()  # op
            self.write_term()
        self.decrease_indent()
        self.add_closing_tag('expression')

    # integerConstant | stringConstant | keywordConstant | varName |
    # varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
    def compile_term(self):
        self.add_opening_tag('term')
        self.increase_indent()
        next_token = self.tokenizer.look_ahead()
        if next_token[1] in unary_ops:
            self.write_next_token()  # unaryOp
            self.compile_term()  # term
        elif next_token[1] == '(':
            self.write_next_token()  # (
            self.compile_expression()  # expression
            self.write_next_token()  # )
        else:  # some sort of identifier is present first
            # varname|subroutineName|className|intconstant|stringconstant|keywordconstant
            self.write_next_token()
            # expression
            if self.tokenizer.look_ahead()[1] == '[':
                self.write_next_token()  # [
                self.write_expression()  # expression
                self.write_next_token()  # ]
            # subroutineCall case 1
            elif self.tokenizer.look_ahead()[1] == '.':
                self.write_next_token()  # .
                self.write_next_token()  # subroutineName
                self.write_next_token()  # (
                self.compile_expression_list()  # expressionList
                self.write_next_token()  # )
            # subroutine case 2
            elif self.tokenizer.look_ahead()[1] == '(':
                self.write_next_token()  # (
                self.compile_expression_list()  # expressionList
                self.write_next_token()  # )
        self.decrease_indent()
        self.add_closing_tag('term')

    # (expression (',' expression)* )?
    def compile_expression_list(self):
        self.add_opening_tag('expressionList')
        self.increase_indent()
        # can there be an expression with a ) in it?
        while self.tokenizer.look_ahead()[1] not in set([')', ']']):
            self.compile_expression()
        self.decrease_indent()
        self.add_closing_tag('expressionList')

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
