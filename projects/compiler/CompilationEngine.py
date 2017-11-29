

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

    def write_next_token(self):
        self.tokenizer.advance()
        token_type = self.tokenizer.get_token_type()
        token = self.tokenizer.get_token_value()
        self.contents.append("\t" * self.indent + "<{token_type}>{token}</{token_type}>"
            .format(token_type=token_type, token=token))

    # 'class' className '{' classVarDec* subroutineDec* '}'
    def compile_class(self):
        self.increase_indent()
        self.add_opening_tag('class')
        self.increase_indent()
        self.write_next_token()  # 'class'
        self.write_next_token()  # className
        self.write_next_token()  # {

        if self.tokenizer.look_ahead()[1] in set(['static', 'field']):
            self.compile_class_var_dec()

        while self.tokenizer.has_more_tokens():
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

    # subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) subroutineName '(' parameterList ')' subroutineBody
    def compile_subroutine(self):
        self.add_opening_tag('subroutineDec')
        self.increase_indent()
        while self.tokenizer.get_token_value() != '(':
            self.write_next_token()
        self.write_next_token()  # (
        self.compile_param_list()
        self.write_next_token()  # )
        self.compile_subroutine_body()
        self.decrease_indent()
        self.add_closing_tag('subroutineDec')

    # subroutineBody: '{' varDec* statements '}'
    def compile_subroutine_body(self):
        self.add_opening_tag('subroutineBody')
        self.increase_indent()
        self.write_next_token()  # {
        while self.tokenizer.get_token_value() != '}':
            if self.tokenizer.get_token_value() == 'var':
                self.compile_var_dec()
            else:
                self.compile_statements()
        self.write_next_token()  # }
        self.decrease_indent()
        self.add_closing_tag('subroutineBody')

    def compile_param_list(self):
        self.add_opening_tag('paramList')
        self.increase_indent()
        while self.tokenizer.get_token_value() != ')':
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
        self.write_closing_tag('statements')

    def compile_do(self):
        pass

    def compile_let(self):
        pass

    def compile_while(self):
        pass

    def compile_return(self):
        pass

    def compile_if(self):
        pass

    def compile_expression(self):
        pass

    def compile_term(self):
        pass

    def compile_expression_list(self):
        pass

    def increase_indent(self):
        self.indent += 1

    def decrease_indent(self):
        self.indent -= 1

    def write_token(self, token):
        token_str = token + "\n"
        self.contents.append(token_str)

    def add_opening_tag(self, tagname):
        tag_str = "/t" * self.indent, "<{}>\n".format(tagname)
        self.contents.append(tag_str)

    def add_closing_tag(self, tagname):
        tag_str = "/t" * self.indent, "</{}>\n".format(tagname)
        self.contents.append(tag_str)
