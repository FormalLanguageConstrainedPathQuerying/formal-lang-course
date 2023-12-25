import antlr4
from pydot import Dot, Node, Edge

from project.parser.QueryLanguageLexer import QueryLanguageLexer
from project.parser.QueryLanguageParser import QueryLanguageParser

from project.parser.dot_listener import DotListener


def parser_of_source(source: str) -> QueryLanguageParser:
    """
    Create antlr4 parser object from source code

    Args:
        source: source code of query language programm

    Returns:
        created parser
    """

    return QueryLanguageParser(
        antlr4.CommonTokenStream(QueryLanguageLexer(antlr4.InputStream(source)))
    )


def check(source: str) -> bool:
    """
    Check if source code is valid query language program

    Args:
        source: source code to check

    Returns:
        True if program is correct, otherwise False
    """

    parser = parser_of_source(source)
    parser.removeErrorListener()
    parser.prog()
    return parser.getNumberOfSyntaxErrors() == 0


def dot_of_source(source: str):
    """
    Parse query language program source code and make a dot file with the program

    Args:
        source: source code to parse

    Returns:
        Dot object containing program
    """

    parser = parser_of_source(source)
    ast = parser.program()

    assert parser.getNumberOfSyntaxErrors() == 0, "Input text has errors"

    listener = DotListener()
    walker = antlr4.ParseTreeWalker()
    walker.walk(listener, ast)

    dot = listener.result

    return dot
