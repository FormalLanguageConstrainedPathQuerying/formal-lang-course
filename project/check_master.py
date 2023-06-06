import os.path

import pydot
from antlr4 import *

from gen.GramLexer import GramLexer
from gen.GramListener import GramListener
from gen.GramParser import GramParser


def is_valid(text: str) -> bool:
    if os.path.isfile(text):
        stream = FileStream(text)
    elif text is None:
        stream = StdinStream()
    else:
        stream = InputStream(text)

    lexer = GramLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = GramParser(token_stream)

    parser.removeErrorListeners()
    parser._errHandler = BailErrorStrategy()

    try:
        parser.prog()
        return True
    except:
        return False


class DotListener(GramListener):
    def __init__(self):
        self.result = pydot.Dot()
        self.curr: list[pydot.Node] = []
        self.names = GramParser(None).ruleNames
        self.node_id = 1

    def enterEveryRule(self, ctx: ParserRuleContext):
        node = pydot.Node(
            str(self.node_id),
            label=self.names[ctx.getRuleIndex()],
            tooltip=ctx.getText(),
        )
        self.node_id += 1
        self.result.add_node(node)
        if len(self.curr) > 0:
            self.result.add_edge(pydot.Edge(self.curr[-1].get_name(), node.get_name()))
        self.curr.append(node)
        super().enterEveryRule(ctx)

    def exitEveryRule(self, ctx: ParserRuleContext):
        self.curr.pop()
        super().exitEveryRule(ctx)


def convert_to_dot(code):
    if os.path.isfile(code):
        stream = FileStream(code)
    elif code is None:
        stream = StdinStream()
    else:
        stream = InputStream(code)

    lexer = GramLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = GramParser(token_stream)
    tree = parser.prog()

    dot_listener = DotListener()

    walker = ParseTreeWalker()
    walker.walk(dot_listener, tree)

    return dot_listener.result