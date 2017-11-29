import re

KEYWORDS = ('(class|constructor|function|method|field|static|var|int|char|'
            'boolean|void|true|false|null|this|let|do|if|else|while|return)')

SYMBOLS = '([{}()[\].,;+\-*/&|<>=~])'

INT_CONSTS = '(\d+)'

STR_CONSTS = '\"([^\n]*)\"'

IDENTIFIERS = '([A-Za-z_]\w*)'

ELEMENT_INDEX_MAP = {
    0: 'keyword',
    1: 'symbol',
    2: 'integer',
    3: 'string',
    4: 'identifier'
}

LEXICAL_ELEMENTS = '{}|{}|{}|{}|{}'.format(KEYWORDS, SYMBOLS, INT_CONSTS,
                   STR_CONSTS, IDENTIFIERS)

MATCH_LEXICAL_ELEMENTS = re.compile(LEXICAL_ELEMENTS)

# regex for inline comment
MATCH_INLINE_COMMENT = re.compile('//.*\n')
# regex for a multiline comment
MATCH_MULTILINE_COMMENT = re.compile('/\*.*?\*/', flags=re.DOTALL)

MATCH_PATTERN = re.compile(LEXICAL_ELEMENTS)


class Tokenizer(object):
    """
    Takes single or multiple .jack files and tokenizes the files
    """
    def __init__(self, file_contents):
        self.file_contents = file_contents
        # takes in a single string with file contents
        self.tokens = self.tokenize()
        self.current = ''

    def has_more_tokens(self):
        """returns true if there are still tokens to be parsed"""
        return len(self.tokens) > 0

    def advance(self):
        """gets next token from the input"""
        self.current = self.tokens.pop(0)

    def get_token_type(self):
        return self.current[0]

    def get_token_value(self):
        return self.current[1]

    def look_ahead(self):
        return self.tokens[1]

    def tokenize(self):
        cleaned_input = self.clean(self.file_contents)
        matches = MATCH_LEXICAL_ELEMENTS.findall(cleaned_input)
        tokens = []
        for match in matches:
            for i, item in enumerate(match):
                if not item:
                    continue
                else:
                    tokens.append((ELEMENT_INDEX_MAP[i], item))
        return tokens

    def clean(self, file_contents):
        """removes whitespace and comments"""
        removed_multiline_contents = re.sub(MATCH_MULTILINE_COMMENT, '', file_contents)
        removed_comments_contents = re.sub(MATCH_INLINE_COMMENT, '', removed_multiline_contents)
        return removed_comments_contents
