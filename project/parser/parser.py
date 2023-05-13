import sys
from pathlib import Path

import antlr4
from antlr4 import *
from project.parser.MyGQLLexer import MyGQLLexer
from project.parser.MyGQLParser import MyGQLParser
from io import StringIO


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = MyGQLLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = MyGQLParser(stream)
    tree = parser.startRule()


if __name__ == "__main__":
    main(sys.argv)


def get_parser_of_stream(inp: InputStream) -> MyGQLParser:
    """
    @param inp: input streams
    @return: parser of input streams
    """
    lexer = MyGQLLexer(inp)
    return MyGQLParser(antlr4.CommonTokenStream(lexer))


def satisfy_lang_inp_stream(inp: InputStream) -> bool:
    """
    Check is text from stream is syntax valid program
    @param inp:  input stream
    @return: true if syntax of program is valid
    """
    parser = get_parser_of_stream(inp)
    parser.removeErrorListeners()
    parser.prog()
    return parser.getNumberOfSyntaxErrors() == 0


def satisfy_lang_str(text: str):
    """
    Check is text is syntax valid program
    @param text: to check
    @return: true if syntax of program is valid
    """
    return satisfy_lang_inp_stream(antlr4.InputStream(text))


def satisfy_lang(filename: str | Path):
    """
    Check is file contains syntax valid program
    @param filename: name of file | path to file
    @return: true if syntax of program is valid
    """
    if isinstance(filename, Path):
        return satisfy_lang_inp_stream(
            antlr4.InputStream("\n".join(filename.open().readlines()))
        )
    else:
        return satisfy_lang_inp_stream(
            antlr4.InputStream("\n".join(open(filename).readlines()))
        )
