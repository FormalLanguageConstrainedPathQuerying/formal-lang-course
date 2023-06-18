from typing import List, Dict, Tuple, TextIO
from dataclasses import dataclass
from antlr4 import *
from ast import literal_eval
import io

from project.parser.MyGQLLexer import MyGQLLexer as Lexer
from project.parser.MyGQLParser import MyGQLParser as Parser
from project.parser.MyGQLVisitor import MyGQLVisitor as Visitor

from project.finite_automata_converters import *
from project.grammar import *
from project.graph_utils import *
from project.parser.MyGQLParser import MyGQLParser
from project.querying import *
from project.rsm import *


class ErrorSyntax(Exception):
    _message: str

    def __init__(self, message: str):
        self._message = message

    def __str__(self):
        return self._message


class ErrorPatternMismatch(ErrorSyntax):
    def __init__(self, mess: str):
        super().__init__(f"Mismatch pattern: {mess}")


class ErrorDoubleVariableInPattern(ErrorSyntax):
    def __init__(self, name: str):
        super().__init__(f"Variable f{name} was duplicated in the pattern")


@dataclass
class FiniteAutomat:
    eNFA: EpsilonNFA


@dataclass
class SetRange:
    flour: int
    upper: int

    def __iter__(self):
        return self

    def __next__(self):
        num = self.flour
        if num == self.upper:
            raise StopIteration()
        self.flour += 1
        return num

    def __contains__(self, item):
        return self.flour <= item < self.upper


class ErrorVisitor(Visitor):
    def __init__(self):
        self.has_error = False

    def visitErrorNode(self, node):
        self.has_error = True


def mapperCollector(output: set, x, fold_x):
    output.add(fold_x)


def filterCollector(out: set, x, fold_x):
    if fold_x:
        out.add(x)


class RunnerVisitor(Visitor):
    _stack: List[Dict[str, Any]]
    _matching_stack: List[Dict[str, Any]]

    def __init__(self, writer: TextIO):
        self._writer = writer
        self._stack = [{}]
        self._collectors_stack: List = []
        self._result_stack: List[frozenset] = [frozenset({})]

    _matched_val: Any = None
    _pattern_dict: Dict[str, Any] = {}

    def _pattern_matching(self, pat: Parser.ArgsGroupContext, val) -> Dict[str, Any]:
        self._matched_val = val
        self._pattern_dict = {}
        if len(pat.children) == 1:
            self.visitArgsSingle(pat)
        else:
            self.visitArgsGroup(pat)
        return self._pattern_dict

    def visitBind(self, ctx: Parser.BindContext):
        dct = self._pattern_matching(ctx.children[1], self.visit(ctx.children[3]))
        for name, val in dct.items():
            if name in self._stack[0]:
                raise ErrorSyntax(f"Double binding of variable {name}")
            self._stack[-1][name] = val

    def visitPrint(self, ctx: Parser.PrintContext):
        val = self.visit(ctx.children[1])
        if hasattr(val, "__iter__"):
            print(sorted(val), file=self._writer)
        else:
            print(val, file=self._writer)

    def visitExprParentheses(self, ctx: Parser.ExprParenthesesContext):
        return self.visit(ctx.children[1])

    def visitLambda(self, ctx: Parser.LambdaContext) -> frozenset:
        out = set()
        pat = ctx.children[0]
        expr = ctx.children[3]
        collector = self._collectors_stack[-1]
        results = self._result_stack.pop()
        layer = self._stack[-1].copy()
        self._stack.append(layer)
        for x in results:
            matched = self._pattern_matching(pat, x)
            for name, val in matched.items():
                layer[name] = val
            fx = self.visit(expr)
            collector(out, x, fx)
        self._stack.pop()
        return frozenset(out)

    def visitExprMap(self, ctx: Parser.ExprMapContext):
        self._collectors_stack.append(mapperCollector)
        result = self._folder(ctx)
        self._collectors_stack.pop()
        return result

    def visitExprFilter(self, ctx: Parser.ExprFilterContext):
        self._collectors_stack.append(filterCollector)
        result = self._folder(ctx)
        self._collectors_stack.pop()
        return result

    def _folder(self, ctx: Parser.ExprContext):
        self._result_stack.append(self.visit(ctx.children[3]))
        result = self.visit(ctx.children[1])
        if not isinstance(result, frozenset):
            raise ErrorSyntax(f"{type(result)} is not a set")
        return result

    def visitArgsSingle(self, ctx: Parser.ArgsSingleContext):
        name = self.visit(ctx.children[0])
        if name is None:
            name = ctx.children[0].symbol.text
        if name in self._pattern_dict:
            raise ErrorDoubleVariableInPattern(name)
        self._pattern_dict[name] = self._matched_val

    def visitArgsGroup(self, ctx: Parser.ArgsGroupContext):
        counter = (ctx.getChildCount() - 1) // 2
        val = self._matched_val
        if not isinstance(val, Tuple):
            raise ErrorPatternMismatch(str(val))
        if len(val) != counter:
            raise ErrorPatternMismatch("error of number of arguments")

        for i in range(counter):
            self._matched_val = val[i]
            self.visit(ctx.children[2 * i + 1])

    def visitVar(self, ctx: Parser.VarContext) -> str:
        return str(ctx.children[0])

    def visitValBool(self, ctx: MyGQLParser.ValBoolContext):
        return bool(str(ctx.children[0]))

    def visitValInt(self, ctx: Parser.ValIntContext) -> int:
        return int(str(ctx.children[0]))

    def visitValString(self, ctx: Parser.ValStringContext) -> str:
        return literal_eval(str(ctx.children[0]))

    def visitEmptySet(self, ctx: Parser.EmptySetContext) -> frozenset:
        return frozenset(set())

    def visitSetElem(self, ctx: Parser.SetElemContext) -> frozenset:
        return frozenset(self.visit(x) for x in ctx.children[1:-1:2])

    def visitSetIntRange(self, ctx: Parser.SetIntRangeContext) -> SetRange:
        return SetRange(self.visit(ctx.children[1]), self.visit(ctx.children[3]))

    def visitExprVar(self, ctx: Parser.ExprVarContext):
        name = self.visit(ctx.children[0])
        if name in self._stack[-1]:
            return self._stack[-1][name]
        else:
            raise ErrorSyntax(f"Variable {name} was not found")

    def visitExprVal(self, ctx: Parser.ExprValContext):
        return self.visit(ctx.children[0])

    # GETTERS
    def visitExprGetVertices(self, ctx: Parser.ExprGetVerticesContext) -> frozenset:
        val = self.visit(ctx.children[1])
        if isinstance(val, FiniteAutomat):
            items = set()
            for x in val.eNFA.states:
                assert isinstance(x, State)
                items.add(x.value)
            return frozenset(items)
        else:
            raise ErrorSyntax(f"Can't get vertices of {str(val)} : {type(val)}")

    def visitExprGetStart(self, ctx: Parser.ExprGetStartContext) -> frozenset:
        val = self.visit(ctx.children[1])
        if isinstance(val, FiniteAutomat):
            return frozenset(x.value for x in val.eNFA.start_states)
        else:
            raise ErrorSyntax(f"Can't get start vertexes of {str(val)} : {type(val)}")

    def visitExprGetFinal(self, ctx: Parser.ExprGetFinalContext) -> frozenset:
        val = self.visit(ctx.children[1])
        if isinstance(val, FiniteAutomat):
            return frozenset(x.value for x in val.eNFA.final_states)
        else:
            raise ErrorSyntax(f"Can't get start vertexes of {str(val)} : {type(val)}")

    def visitExprGetEdges(self, ctx: Parser.ExprGetEdgesContext) -> frozenset:
        val = self.visit(ctx.children[1])
        if isinstance(val, FiniteAutomat):
            result_set = set()
            for u, symbol, v in val.eNFA:
                assert isinstance(u, State)
                assert isinstance(symbol, Symbol)
                assert isinstance(v, State)
                assert isinstance(symbol.value, str)
                result_set.add((u.value, symbol.value, v.value))
            return frozenset(result_set)
        else:
            raise ErrorSyntax(f"Can't get edges of {str(val)} : {type(val)}")

    def visitExprGetLabels(self, ctx: Parser.ExprGetLabelsContext) -> frozenset:
        val = self.visit(ctx.children[1])
        if isinstance(val, FiniteAutomat):
            items = set()
            for u, symbol, v in val.eNFA:
                assert isinstance(symbol.value, str)
                items.add(symbol.value)
            return frozenset(items)
        else:
            raise ErrorSyntax(f"Can't get edges of {str(val)} : {type(val)}")

    def visitExprGetReachable(self, ctx: Parser.ExprGetReachableContext) -> frozenset:
        val = self.visit(ctx.children[1])
        if not isinstance(val, FiniteAutomat):
            raise ErrorSyntax(f"Can't get reachable of {str(val)} : {type(val)}")
        return frozenset(
            find_accessible_nodes_of_nfa(val.eNFA, Regex.from_python_regex(".*"))
        )

    def visitExprSetStart(self, ctx: Parser.ExprSetStartContext) -> FiniteAutomat:
        val = self.visit(ctx.children[1])
        if not isinstance(val, frozenset):
            raise ErrorSyntax(f"{str(val)} : {type(val)} is not a set")

        graph = self.visit(ctx.children[3])
        if isinstance(graph, FiniteAutomat):
            fa = graph.eNFA.copy()
            for x in fa.start_states.copy():
                fa.remove_start_state(x)
            for x in val:
                fa.add_start_state(x)
            return FiniteAutomat(fa)
        else:
            raise ErrorSyntax(
                f"Can't set start vertexes to {str(graph)} : {type(graph)}"
            )

    def visitExprSetFinal(self, ctx: Parser.ExprSetFinalContext) -> FiniteAutomat:
        val = self.visit(ctx.children[1])
        if not isinstance(val, frozenset):
            raise ErrorSyntax(f"{str(val)} : {type(val)} is not a set")

        graph = self.visit(ctx.children[3])
        if isinstance(graph, FiniteAutomat):
            fa = graph.eNFA.copy()
            for x in fa.final_states.copy():
                fa.remove_final_state(x)
            for x in val:
                fa.add_final_state(x)
            return FiniteAutomat(fa)
        else:
            raise ErrorSyntax(
                f"Can't set final vertexes to {str(graph)} : {type(graph)}"
            )

    def visitExprAddStart(self, ctx: Parser.ExprAddStartContext) -> FiniteAutomat:
        val = self.visit(ctx.children[1])
        if not isinstance(val, frozenset):
            raise ErrorSyntax(f"{str(val)} : {type(val)} is not a set")

        graph = self.visit(ctx.children[3])
        if isinstance(graph, FiniteAutomat):
            fa = graph.eNFA.copy()
            for x in val:
                fa.add_start_state(x)
            return FiniteAutomat(fa)
        else:
            raise ErrorSyntax(
                f"Can't add start vertexes to type {str(graph)} : {type(graph)}"
            )

    def visitExprAddFinal(self, ctx: Parser.ExprAddFinalContext) -> FiniteAutomat:
        val = self.visit(ctx.children[1])
        if not isinstance(val, frozenset):
            raise ErrorSyntax(f"{str(val)} : {type(val)} is not a set")

        graph = self.visit(ctx.children[3])
        if isinstance(graph, FiniteAutomat):
            fa = graph.eNFA.copy()
            for x in val:
                fa.add_final_state(x)
            return FiniteAutomat(fa)
        else:
            raise ErrorSyntax(
                f"Can't add final vertexes to type {str(graph)} : {type(graph)}"
            )

    def visitExprLoad(self, ctx: Parser.ExprLoadContext):
        path = self.visit(ctx.children[1])
        if not isinstance(path, str):
            raise ErrorSyntax(f"Path should be a string, but is {type(path)}")
        graph = nx_pydot.read_dot(path)
        fa = FAConverters.graph_to_nfa(
            graph, list(graph.nodes)[0], list(graph.nodes)[-1]
        )
        return FiniteAutomat(fa)

    def visitExprShift(self, ctx: Parser.ExprShiftContext) -> FiniteAutomat:
        val = self.visit(ctx.children[0])
        graph = self.visit(ctx.children[2])
        if isinstance(val, str):
            nfa = EpsilonNFA()
            nfa.add_start_state(State(0))
            nfa.add_final_state(State(1))
            nfa.add_transition(State(0), Symbol(val), State(1))
            return FiniteAutomat(nfa.concatenate(graph))
        else:
            raise ErrorSyntax(f"{str(val)} : {type(val)} is not a symbol")

    def visitExprIntersect(self, ctx: Parser.ExprIntersectContext):
        fa1 = self.visit(ctx.children[0])
        fa2 = self.visit(ctx.children[2])
        if not isinstance(fa1, FiniteAutomat) or not isinstance(fa2, FiniteAutomat):
            raise ErrorSyntax(f"Can't intersect {type(fa1)} and {type(fa2)}")
        return FiniteAutomat(
            TensorNFA.from_nfa(fa1.eNFA)
            .intersect(TensorNFA.from_nfa(fa2.eNFA))
            .to_nfa()
        )

    def visitExprUnion(self, ctx: Parser.ExprUnionContext):
        fa1 = self.visit(ctx.children[0])
        fa2 = self.visit(ctx.children[2])
        if isinstance(fa1, FiniteAutomat) and isinstance(fa2, FiniteAutomat):
            return FiniteAutomat(fa1.eNFA.copy().union(fa2.eNFA))
        else:
            raise ErrorSyntax(f"Can't intersect {type(fa1)} and {type(fa2)}")

    def visitExprConcat(self, ctx: Parser.ExprConcatContext):
        fa1 = self.visit(ctx.children[0])
        fa2 = self.visit(ctx.children[2])

        if isinstance(fa1, FiniteAutomat) and isinstance(fa2, FiniteAutomat):
            return FiniteAutomat(fa1.eNFA.concatenate(fa2.eNFA))
        else:
            raise ErrorSyntax(f"Can't concat {type(fa1)} with {type(fa2)}")

    def visitExprKlini(self, ctx: Parser.ExprKliniContext):
        val = self.visit(ctx.children[0])
        if isinstance(val, FiniteAutomat):
            return FiniteAutomat(val.eNFA.kleene_star())
        else:
            raise ErrorSyntax(f"Can't Kline close {str(val)} : {type(val)}")

    def visitExprInChecking(self, ctx: Parser.ExprInCheckingContext) -> bool:
        val1 = self.visit(ctx.children[0])
        val2 = self.visit(ctx.children[2])

        if not hasattr(val2, "__contains__"):
            raise ErrorSyntax(
                f"The second operand of `in` is {type(val2)} must be container"
            )
        return val1 in val2


def _parse_tree(reader: InputStream, suppress_errors=False):
    lexer = Lexer(reader)
    if suppress_errors:
        lexer.removeErrorListeners()
    parser = Parser(CommonTokenStream(lexer))
    if suppress_errors:
        parser.removeErrorListeners()
    return parser.prog()


def interpret(program: Parser.ProgContext, writer: TextIO):
    """
    Do interpretation of Parser.ProgContext
    @param program: Parser.ProgContext to interpret
    @param writer:  output stream
    """
    error_visitor = ErrorVisitor()
    error_visitor.visit(program)
    if error_visitor.has_error:
        print("Stop: lexical error", file=writer)
        return
    try:
        RunnerVisitor(writer).visit(program)
    except ErrorSyntax as e:
        print(e, file=writer)
        print("Stop: syntax error", file=writer)
        return


def interpret_string_to_writer(s: str, writer: TextIO):
    """
    Interpret text of program to output stream
    @param s: text of program
    @param writer: output stream
    """
    tree = _parse_tree(InputStream(s))
    interpret(tree, writer)


def interpret_string(s: str) -> str:
    """
    Interpret text of program
    @param s: text of program
    @return: output of program
    """
    with io.StringIO() as writer:
        interpret_string_to_writer(s, writer)
        return writer.getvalue()
