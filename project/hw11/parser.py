import antlr4
from antlr4.tree.Tree import TerminalNode
from antlr4 import ParserRuleContext
from project.hw11.GLparserParser import GLparserParser
from project.hw11.GLparserLexer import GLparserLexer


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


def nodes_count(tree: ParserRuleContext) -> int:
    if tree is None:
        return 0
    count = 0
    for i in range(tree.getChildCount()):
        child = tree.getChild(i)
        count += nodes_count(child)
    return count


def tree_to_program(tree: ParserRuleContext) -> str:
    if tree is None:
        return ""

    reconstructed_string = ""
    for child in tree.getChildren():
        if isinstance(child, TerminalNode):
            if child.getText() != "<EOF>":
                reconstructed_string += child.getText() + " "
            else:
                reconstructed_string += "\n"

        else:
            reconstructed_string += tree_to_program(child)
    return reconstructed_string
