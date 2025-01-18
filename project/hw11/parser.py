import antlr4
from antlr4 import ParserRuleContext
from project.hw11.GLparserParser import GLparserParser
from project.hw11.GLparserLexer import GLparserLexer


class Listener(antlr4.ParseTreeListener):
    def __init__(self):
        self.tokens = []
        self.count = 0

    def visitTerminal(self, node):
        self.tokens.append(node.getText())

    def enterEveryRule(self, ctx):
        self.count += 1


def program_to_tree(program: str) -> tuple[ParserRuleContext, bool]:
    input_stream = antlr4.InputStream(program)
    lexer = GLparserLexer(input_stream)
    stream = antlr4.CommonTokenStream(lexer)
    parser = GLparserParser(stream)
    tree = parser.prog()
    errors = parser.getNumberOfSyntaxErrors()
    if errors != 0:
        return tree, False
    return tree, True


def nodes_count(tree: antlr4.ParserRuleContext) -> int:
    if not tree:
        return 0

    listener = Listener()
    walker = antlr4.ParseTreeWalker()
    walker.walk(listener, tree)

    return listener.count


def tree_to_program(tree: antlr4.ParserRuleContext) -> str:
    if not tree:
        return ""
    listener = Listener()
    walker = antlr4.ParseTreeWalker()
    walker.walk(listener, tree)
    return " ".join(listener.tokens)

# program_to_tree()