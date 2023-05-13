import sys
from pathlib import Path

import antlr4
import pydot
from antlr4 import *
from project.parser.MyGQLLexer import MyGQLLexer
from project.parser.MyGQLParser import MyGQLParser
from project.parser.MyGQLListener import MyGQLListener


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


def parse_tree_to_dot_file(inp: InputStream, path: str | Path):
    """
    Generates a description of the parse tree
    for a given input stream to a dot file
    @param inp: input stream
    @param path: path of file to save
    """
    parser = get_parser_of_stream(inp)
    if parser.getNumberOfSyntaxErrors() > 0:
        raise ValueError("Invalid syntax")
    builder = _MyGQLToDotListener()
    walker = antlr4.ParseTreeWalker()
    walker.walk(builder, parser.prog())
    builder.dot.write(str(path))


def parse_tree_str_to_dot_file(text: str, path: str | Path):
    """
    Generates a description of the parse tree
    for a given input text to a dot file
    @param text: input text
    @param path: path of file to save
    """
    parse_tree_to_dot_file(InputStream(text), path)


class _MyGQLToDotListener(MyGQLListener):
    def __init__(self):
        self.dot = pydot.Dot("parse_tree", strict=True)
        self._index = 1
        self._stack = [0]

    def enterEveryRule(self, ctx: antlr4.ParserRuleContext):
        self.dot.add_node(
            pydot.Node(self._index, label=MyGQLParser.ruleNames[ctx.getRuleIndex()])
        )
        self.dot.add_edge(pydot.Edge(self._stack[-1], self._index))
        self._stack.append(self._index)
        self._index += 1

    def exitEveryRule(self, ctx: antlr4.ParserRuleContext):
        self._stack.pop()

    def visitTerminal(self, node: antlr4.TerminalNode):
        self.dot.add_node(pydot.Node(self._index, label=f"'{node}'", shape="box"))
        self.dot.add_edge(pydot.Edge(self._stack[-1], self._index))
        self._index += 1
