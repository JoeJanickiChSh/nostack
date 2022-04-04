

class Token:
    DECLARE = "DECLARE"
    STATEMENT = "STATEMENT"
    INTEGER = "TYPE_INTEGER"
    FLOAT = "TYPE_FLOAT"
    VARIABLE = "VARIABLE"
    FUNCTION = "FUNCTION"
    OP_ASSIGN = "OP_ASSIGN"
    OP_BINARY = "OP_BINARY"
    END = "END"
    PAR_OPEN = "PAR_OPEN"
    PAR_CLOSE = "PAR_CLOSE"
    BRAC_OPEN = "BRAC_OPEN"
    BRAC_CLOSE = "BRAC_CLOSE"
    LIST_OPEN = "LIST_OPEN"
    LIST_CLOSE = "LIST_CLOSE"
    COMMA = "COMMA"

    def __init__(self, token_type, value=None):
        self.token_type = token_type
        self.value = value

    def __repr__(self):
        return f'{self.token_type}: {self.value}'


NUMS = '0123456789'
LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTYVWXYZ:'
SYMBOLS = '=+-*/%><!&|^~?'
TYPE_SEPERATORS = '_'
STATEMENTS = ['if', 'else', 'elif', 'while']

OPS_ASSIGNMENT = ['=', '+=', '-=', '*=', '/=',
                  '%=', '&=', '|=', '>>=', '<<=', '^=', '?=', '?+', '?-']
OPS_BINARY = ['==', '!=', '+', '-', '*', '/',
              '%', '>', '<', '>=', '<=', '&&', '||', '!', '&', '|', '^', '~', '>>', '<<']

PRIMITIVE_TYPES = [Token.INTEGER, Token.FLOAT]


class Lexer:
    def __init__(self, code):
        self.code = code
        self.point = -1
        self.tokens = []

    def safe_index(self, index):
        return max(0, min(len(self.code)-1, index))

    def get_char(self):
        if self.point in range(len(self.code)):
            return self.code[self.point]
        return ''

    def slice(self, min, max):
        return self.code[self.safe_index(self.point + min): self.safe_index(self.point + max) + 1]

    def advance(self):

        self.point += 1
        if self.get_char() == ';':
            self.tokens.append(Token(Token.END))
        elif self.get_char() == ',':
            self.tokens.append(Token(Token.COMMA))
        elif self.get_char() == '(':
            self.tokens.append(Token(Token.PAR_OPEN))
        elif self.get_char() == ')':
            self.tokens.append(Token(Token.PAR_CLOSE))
        elif self.get_char() == '{':
            self.tokens.append(Token(Token.BRAC_OPEN))
        elif self.get_char() == '}':
            self.tokens.append(Token(Token.BRAC_CLOSE))
        elif self.get_char() == '[':
            self.tokens.append(Token(Token.LIST_OPEN))
        elif self.get_char() == ']':
            self.tokens.append(Token(Token.LIST_CLOSE))
        elif self.get_char() == '_':
            if self.slice(-3, -1) == 'int':
                self.tokens.append(Token(Token.DECLARE, Token.INTEGER))
            elif self.slice(-5, -1) == 'float':
                self.tokens.append(Token(Token.DECLARE, Token.FLOAT))
            elif self.slice(-4, -1) == 'func':
                self.tokens.append(Token(Token.DECLARE, Token.FUNCTION))

        elif self.get_char() in NUMS:
            num_val = ''
            dot_count = 0
            while self.get_char() in (NUMS + '.') and self.get_char() != '':
                num_val += self.get_char()
                if self.get_char() == '.':
                    dot_count += 1
                self.point += 1
            self.point -= 1
            if dot_count == 0:
                self.tokens.append(Token(Token.INTEGER, num_val))
            elif dot_count == 1:
                self.tokens.append(Token(Token.FLOAT, num_val))
            else:
                pass

        elif self.get_char() in LETTERS:
            var_val = ''
            og_point = self.point
            while self.get_char() in LETTERS and self.get_char() != '':
                var_val += self.get_char()
                self.point += 1
            if self.get_char() in TYPE_SEPERATORS and self.get_char() != '':
                self.point = og_point
            elif self.get_char() == '|':
                self.tokens.append(Token(Token.FUNCTION, var_val))
            elif var_val in STATEMENTS:
                self.point -= 1
                self.tokens.append(Token(Token.STATEMENT, var_val))
            else:
                self.point -= 1
                self.tokens.append(Token(Token.VARIABLE, var_val))

        elif self.get_char() in SYMBOLS:
            var_val = ''
            og_point = self.point
            while self.get_char() in SYMBOLS and self.get_char() != '':
                var_val += self.get_char()
                self.point += 1
            self.point -= 1
            if var_val in OPS_ASSIGNMENT:
                self.tokens.append(Token(Token.OP_ASSIGN, var_val))
            elif var_val in OPS_BINARY:
                self.tokens.append(Token(Token.OP_BINARY, var_val))

    def lex(self):
        self.point = -1
        self.tokens = []
        while(self.point < len(self.code)-1):
            self.advance()
        return self.tokens


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self):
        out_lines = []
        line = []
        for t in self.tokens:
            line.append(t)
            if t.token_type in [Token.END, Token.BRAC_OPEN, Token.BRAC_CLOSE]:
                out_lines.append(line)
                line = []
        return out_lines
