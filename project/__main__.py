import sys
from antlr4 import *

from project.parser.MyGQLLexer import MyGQLLexer
from project.parser.MyGQLParser import MyGQLParser

from project.interpreter import interpret


def main(args):
    parser = MyGQLParser(CommonTokenStream(MyGQLLexer(StdinStream(encoding="utf-8"))))
    interpret(parser.prog(), sys.stdout)


if __name__ == "__main__":
    main(sys.argv)
