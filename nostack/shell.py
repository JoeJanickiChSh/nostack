import sys
from preprocess import PreProcessor
from lang import Lexer, Parser


def main(argv):

    with open(argv[1], 'r') as fp:
        code = fp.read()
    ppc = PreProcessor(code)
    lexer = Lexer(ppc.process())
    parser = Parser(lexer.lex())
    lines = parser.parse()
    for line in lines:
        print(line)


if __name__ == '__main__':
    main(sys.argv)
