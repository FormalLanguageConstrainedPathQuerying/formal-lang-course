from antlr4 import *
from pyformlang.finite_automaton import EpsilonNFA as Automata, State
from pyformlang.finite_automaton.epsilon import Epsilon
from pyformlang.regular_expression import Regex

from project.my_lang.automata import build_dfa_from_graph, get_graph
import sys

import networkx as nx
from gen.GramLexer import GramLexer
from gen.GramParser import GramParser
from gen.GramVisitor import GramVisitor


def iterable(obj: object) -> bool:
    return hasattr(obj, '__iter__')


class MyEx(Exception):
    def __init__(self, message):
        self.message = message


class BindEx(MyEx):
    def __init__(self, name):
        self.name = name
        self.message = f'Can not bind var \'{name}\' because this var already exists.'


class AssignEx(MyEx):
    def __init__(self, name):
        self.name = name
        self.message = f'Can not assign var \'{name}\' because this var does not exist.'


class IterableEx(MyEx):
    def __init__(self, obj):
        self.obj = obj
        self.message = f'Object {obj} of type {type(obj)} is not iterable.'


class UnionEx(MyEx):
    def __init__(self, e1, e2):
        self.message = f'Objects {e1} and {e2} of types {type(e1)} and {type(e2)} can not product union.'


class IntersectEx(MyEx):
    def __init__(self, e1, e2):
        self.message = f'Objects {e1} and {e2} of types {type(e1)} and {type(e2)} can not product intersection.'


class ConcatEx(MyEx):
    def __init__(self, e1, e2):
        self.message = f'Objects {e1} and {e2} of types {type(e1)} and {type(e2)} can not product concat.'


class DifferentTypesEx(MyEx):
    def __init__(self, e1, e2):
        self.message = f'Objects {e1} and {e2} have different types: {type(e1)} and {type(e2)}.'


class KleeneEx(MyEx):
    def __init__(self, obj):
        self.message = f'Can not make kleene with object {obj}.'


class UnexpectedNameEx(MyEx):
    def __init__(self, name):
        self.name = name
        self.message = f'No variable with name \'{name}\'.'


class Env:
    def __init__(self):
        self.vars = dict()

    def __contains__(self, name):
        return name in self.vars

    def __getitem__(self, name: str):
        return self.vars[name]

    def __setitem__(self, name, value):
        self.vars[name] = value


class MyVisitor(GramVisitor):

    def __init__(self):
        self.env = Env()

    def visitPrint(self, ctx: GramParser.PrintContext):
        expr = self.visit(ctx.expr())
        if isinstance(expr, Automata):
            print(nx.nx_pydot.to_pydot(expr.to_networkx()).to_string())
        else:
            print(expr)

    def visitBind(self, ctx: GramParser.BindContext):
        name = ctx.name().getText()
        if name in self.env:
            raise BindEx(name)
        self.env[name] = self.visit(ctx.expr())

    def visitAssign(self, ctx:GramParser.AssignContext):
        name = ctx.name().getText()
        if name not in self.env:
            raise AssignEx(name)
        self.env[name] = self.visit(ctx.expr())

    def visitLambda(self, ctx: GramParser.LambdaContext):
        name = ctx.name().getText()
        code = ctx.CODE().getText()[1: -1]

        def func(s):
            result = list()
            for j in s:
                i = j
                if isinstance(s, Automata) and isinstance(i[1], Epsilon) and isinstance(i[1], Epsilon):
                    i = (i[0], 'epsilon', i[2])
                context = dict()
                exec(f"result = (lambda {name}:{code})({i})", self.env.vars, context)
                result.append(context["result"])
            return result

        return func

    def visitMap(self, ctx: GramParser.MapContext):
        f = self.visitLambda(ctx.lambda_())
        e = self.visit(ctx.expr())

        if not iterable(e):
            raise IterableEx(e)

        return f(e)

    def visitFilter(self, ctx: GramParser.FilterContext):
        f = self.visitLambda(ctx.lambda_())
        e = self.visit(ctx.expr())
        r = []

        if not iterable(e):
            raise IterableEx(e)

        for flag, val in zip(f(e), e):
            if not isinstance(flag, bool):
                raise MyEx(f"Filter function {f.__name__} is invalid")
            if flag:
                r.append(val)
        return r

    def visitConstruct(self, ctx: GramParser.ConstructContext):
        s = ctx.str_().getText()
        return Regex(s).to_epsilon_nfa()

    def visitIntAssign(self, ctx: GramParser.IntAssignContext):
        return int(ctx.int_().getText())

    def visitLoad(self, ctx: GramParser.LoadContext):
        path = ctx.PATH().getText()[2:-1]
        return build_dfa_from_graph(get_graph(path))

    def visitAdd(self, ctx: GramParser.AddContext):
        expr = self.visit(ctx.expr()[0])
        states = self.visit(ctx.expr()[1])
        is_start = ctx.sa_state().getText() == 'start'

        if not isinstance(expr, Automata):
            raise MyEx('Can not set states of not EpsilonNFA.')

        if iterable(states):
            states = set(states)
        else:
            raise IterableEx(states)

        if is_start:
            expr.start_states.update(states)
        else:
            expr.final_states.update(states)
        return expr

    def visitUnion(self, ctx: GramParser.UnionContext):
        e1 = self.visit(ctx.expr()[0])
        e2 = self.visit(ctx.expr()[1])

        if isinstance(e1, Automata) and isinstance(e2, Automata):
            return e1.union(e2)
        elif isinstance(e1, set) and isinstance(e2, set):
            return e1.union(e2)
        elif isinstance(e1, list) and isinstance(e2, list):
            return e1 + e2
        else:
            raise UnionEx(e1, e2)

    def visitNameAssign(self, ctx: GramParser.NameAssignContext):
        name = ctx.name().getText()
        if name not in self.env:
            raise UnexpectedNameEx(name)
        return self.env[name]

    def visitStringAssign(self, ctx: GramParser.StringAssignContext):
        return ctx.STRING().getText()

    def visitSet(self, ctx: GramParser.SetContext):
        expr = self.visit(ctx.expr()[0])
        states = self.visit(ctx.expr()[1])
        is_start = ctx.sa_state().getText() == 'start'

        if not isinstance(expr, Automata):
            raise MyEx('Can not set states of not EpsilonNFA.')

        if iterable(states):
            states = set(states)
        else:
            raise IterableEx(states)

        if is_start:
            expr.start_states.clear()
            expr.start_states.update(states)
        else:
            expr.final_states.clear()
            expr.final_states.update(states)
        return expr

    def visitIntersect(self, ctx: GramParser.IntersectContext):
        e1 = self.visit(ctx.expr()[0])
        e2 = self.visit(ctx.expr()[1])

        if isinstance(e1, Automata) and isinstance(e2, Automata):
            return e1.get_intersection(e2)
        elif isinstance(e1, set) and isinstance(e2, set):
            return e1.intersection(e2)
        elif isinstance(e1, list) and isinstance(e2, list):
            return list(set(e1).intersection(set(e2)))
        else:
            raise IntersectEx(e1, e2)

    def visitBracket(self, ctx: GramParser.BracketContext):
        return self.visit(ctx.expr())

    def visitKleene(self, ctx: GramParser.KleeneContext):
        e = self.visit(ctx.expr())

        if not isinstance(e, Automata):
            raise KleeneEx(e)

        return e.kleene_star()

    def visitUnequals(self, ctx: GramParser.UnequalsContext):
        e1 = self.visit(ctx.expr()[0])
        e2 = self.visit(ctx.expr()[1])
        if isinstance(e1, Automata) and isinstance(e2, Automata):
            return not e1.is_equivalent_to(e2)
        elif type(e1) != type(e2):
            raise DifferentTypesEx(e1, e2)
        else:
            return e1 != e2

    def visitEquals(self, ctx: GramParser.EqualsContext):
        e1 = self.visit(ctx.expr()[0])
        e2 = self.visit(ctx.expr()[1])
        if isinstance(e1, Automata) and isinstance(e2, Automata):
            return e1.is_equivalent_to(e2)
        elif type(e1) != type(e2):
            raise DifferentTypesEx(e1, e2)
        else:
            return e1 == e2

    def visitConcat(self, ctx: GramParser.ConcatContext):
        e1 = self.visit(ctx.expr()[0])
        e2 = self.visit(ctx.expr()[1])

        if isinstance(e1, Automata) and isinstance(e2, Automata):
            return e1.concatenate(e2)
        elif isinstance(e1, set) and isinstance(e2, set):
            return e1.union(e2)
        elif isinstance(e1, list) and isinstance(e2, list):
            return e1 + e2
        else:
            raise ConcatEx(e1, e2)

    def visitGet(self, ctx: GramParser.GetContext):
        state_type = ctx.get_state().getText()
        expr = self.visit(ctx.expr())

        if not isinstance(expr, Automata):
            raise MyEx('Can not set states of not EpsilonNFA.')

        if state_type == 'start':
            return expr.start_states
        elif state_type == 'final':
            return expr.final_states
        elif state_type == 'reachable':
            g: nx.MultiDiGraph = nx.transitive_closure(nx.DiGraph(expr.to_networkx()))
            return g.edges
        elif state_type == 'nodes':
            return expr.states
        elif state_type == 'edges':
            return set(expr)
        elif state_type == 'labels':
            return expr.symbols

    def visitEmptyList(self, ctx: GramParser.EmptyListContext):
        return []

    def visitList(self, ctx: GramParser.ListContext):
        r = []
        for i in range(ctx.getChildCount() // 2):
            r.append(self.visit(ctx.expr(i)))
        return r

    def visitEmptySet(self, ctx: GramParser.EmptySetContext):
        return set()

    def visitBigSet(self, ctx: GramParser.BigSetContext):
        r = set()
        for i in range(ctx.getChildCount() // 2):
            r.add(self.visit(ctx.expr(i)))
        return r


def do(path: str = 'my_code.txt'):
    with open(path, 'r') as infile:
        execute_code(infile.read())


def execute_code(code: str):
    print(code)
    data = InputStream(code)
    lexer = GramLexer(data)
    stream = CommonTokenStream(lexer)
    parser = GramParser(stream)
    tree = parser.prog()
    visitor = MyVisitor()
    _ = visitor.visit(tree)


if __name__ == '__main__':
    do(sys.argv[0])
