import sys

from project.hw12.interpreter_visitor import InterpreterVisitor
from project.hw11.parser import program_to_tree
from project.hw11.GLparserVisitor import GLparserVisitor


def interpret(code: str):

    tree = program_to_tree(code)
    visitor = InterpreterVisitor()
    res = visitor.visit(tree[0])
    return visitor

if __name__ == '__main__':
    interp = interpret('let q = a | c | b')
    print(interp)