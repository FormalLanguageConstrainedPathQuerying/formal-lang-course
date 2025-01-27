from antlr4.CommonTokenStream import CommonTokenStream
from antlr4.InputStream import InputStream

from project.hw12.interpreter_visitor import InterpreterVisitor
from project.hw12.type_inference import GLTypesInferencer
from project.hw11.GLparserLexer import GLparserLexer
from project.hw11.GLparserParser import GLparserParser


def typing_program(program: str) -> bool:
    lexer = GLparserLexer(InputStream(program))
    stream = CommonTokenStream(lexer)
    parser = GLparserParser(stream)
    tree = parser.prog()
    types_visitor = GLTypesInferencer()
    try:
        types_visitor.visit(tree)
        return True
    except Exception:
        return False


def exec_program(program: str) -> dict[str, set[tuple]]:
    lexer = GLparserLexer(InputStream(program))
    stream = CommonTokenStream(lexer)
    parser = GLparserParser(stream)
    tree = parser.prog()
    runner_visitor = InterpreterVisitor()
    try:
        runner_visitor.visit(tree)
        return runner_visitor.last_query_results
    except Exception:
        return {}
