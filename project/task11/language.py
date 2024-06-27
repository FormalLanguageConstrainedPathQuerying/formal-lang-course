from antlr4 import InputStream, CommonTokenStream
from gen.TestLexer import TestLexer
from gen.TestParser import TestParser
from antlr4.ParserRuleContext import ParserRuleContext


def prog_to_tree(program: str) -> tuple[ParserRuleContext, bool]:
    """
    Converts program to the parse tree and returns it along with the validity flag.

    """
    lexer = TestLexer(InputStream(program))
    stream = CommonTokenStream(lexer)
    parser = TestParser(stream)
    tree = parser.prog()
    return tree, parser.getNumberOfSyntaxErrors() == 0


def nodes_count(tree: ParserRuleContext) -> int:
    """
    Returns the number of nodes in the tree.
    :param tree:
    :return:
    """

    count = 0
    stack = [tree]

    while stack:
        node = stack.pop()
        count += 1
        for i in range(node.getChildCount()):
            stack.append(node.getChild(i))

    return count


def tree_to_prog(tree: ParserRuleContext) -> str:
    """
    Converts the parse tree to the program.

    :param tree:
    :return:
    """
    if tree is None:
        return ""

    result = []

    def walk_tree(node: ParserRuleContext):
        if node.getChildCount() == 0:
            result.append(node.getText())
        else:
            for i in range(node.getChildCount()):
                walk_tree(node.getChild(i))

    walk_tree(tree)
    return " ".join(result)
