from project.lang.langLexer import langLexer
from project.lang.langParser import langParser
from project.lang.langListener import langListener

from antlr4 import ParserRuleContext, CommonTokenStream
from antlr4.InputStream import InputStream


class NodeCountListener(langListener):

    def __init__(self) -> None:
        super(langListener, self).__init__()
        self.count = 0

    def enterEveryRule(self, ctx):
        self.count += 1

    def get_count(self):
        return self.count


class StringifyListener(langListener):

    def __init__(self):
        super(langListener, self).__init__()
        self.result = ""

    def enterEveryRule(self, rule):
        self.result += rule.getText()

    def get_result(self):
        return self.result


def prog_to_tree(program: str) -> tuple[ParserRuleContext, bool]:
    parser = langParser(CommonTokenStream(langLexer(InputStream(program))))
    return parser.prog(), (parser.getNumberOfSyntaxErrors() == 0)


def nodes_count(tree: ParserRuleContext) -> int:
    listener = NodeCountListener()
    tree.enterRule(listener)
    return listener.get_count()


def tree_to_prog(tree: ParserRuleContext) -> str:
    listener = StringifyListener()
    tree.enterRule(listener)
    return listener.get_result()
