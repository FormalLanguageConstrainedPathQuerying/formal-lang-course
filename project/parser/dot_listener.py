from project.parser.QueryLanguageListener import QueryLanguageListener
from project.parser.QueryLanguageParser import QueryLanguageParser
from pydot import Dot, Edge, Node
from antlr4 import ParserRuleContext
from antlr4.tree.Tree import TerminalNodeImpl


class DotListener(QueryLanguageListener):
    def __init__(self):
        self.result = Dot("program", graph_type="digraph", strict=True)
        self._node_count = 0
        self._nodes = {}
        self._rules = QueryLanguageParser.ruleNames

    def enterEveryRule(self, ctx: ParserRuleContext):
        if ctx not in self._nodes:
            self._node_count += 1
            self._nodes[ctx] = self._node_count

        if ctx.parentCtx:
            self.result.add_edge(Edge(self._nodes[ctx.parentCtx], self._nodes[ctx]))

        label = self._rules[ctx.getRuleIndex()]
        self.result.add_node(Node(self._nodes[ctx], label=label))

    def visitTerminal(self, node: TerminalNodeImpl):
        self._node_count += 1

        self.result.add_node(Node(self._node_count, label=f"{node.getText()}"))
        self.result.add_edge(Edge(self._nodes[node.parentCtx], self._node_count))
