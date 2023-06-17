import sys
from antlr4 import *
from pyformlang.finite_automaton import DeterministicFiniteAutomaton as Automata, State

import networkx as nx
import cfpq_data
from gen.GramLexer import GramLexer
from gen.GramParser import GramParser
from gen.GramVisitor import GramVisitor


def get_username():
    from pwd import getpwuid
    from os import getuid
    return getpwuid(getuid())[0]


def get_graph(name):
    return cfpq_data.graph_from_csv(cfpq_data.download(name))


def build_dfa_from_graph(
    graph: nx.DiGraph, start: set[State] = None, final: set[State] = None
) -> Automata:
    """
    Builds NDFA from graph representation, start and final nodes
    :param graph: Graph representation of the resulting NDFA
    :param start: Start states of the resulting NDFA. If None - all states are considered start states
    :param final: Final states of the resulting NDFA. If None - all states are considered final states
    :return: NDFA built from graph representation, start and final nodes
    """
    dfa = Automata.from_networkx(graph)

    for s, f, label in graph.edges(data="label"):
        dfa.add_transition(s, label, f)

    if start is not None:
        for s in start:
            dfa.add_start_state(s)
    else:
        for s in dfa.states:
            dfa.add_start_state(s)
    if final is not None:
        for s in final:
            dfa.add_final_state(s)
    else:
        for s in dfa.states:
            dfa.add_final_state(s)

    return dfa


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

    def visitProg(self, ctx: GramParser.ProgContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GramParser#statement.
    def visitStatement(self, ctx: GramParser.StatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GramParser#print.
    def visitPrint(self, ctx: GramParser.PrintContext):
        name = ctx.name().getText()
        if name in self.env:
            value = self.env[name]
            print(value)
        else:
            raise 'No such var!'

    # Visit a parse tree produced by GramParser#bind.
    def visitBind(self, ctx: GramParser.BindContext):
        name = ctx.name().getText()
        if name not in self.env:
            c: GramParser.ExprContext = ctx.expr()
            value = self.visit(c)
            self.env[name] = value
        else:
            raise 'This var already exists!'

    # Visit a parse tree produced by GramParser#lambda.
    def visitLambda(self, ctx: GramParser.LambdaContext):
        name = ctx.name().getText()
        c: GramParser.ExprContext = ctx.expr()
        code = self.visit(c)

        id = c.accept(self)

        def func(s):
            result = list()
            for i in s:
                context = dict()
                exec(f"result = (lambda {id.value}:{code})({i})", self.env.vars, context)
                result.append(context["result"])
            return result

        return func

    def visitOne_symbol_expr(self, ctx: GramParser.One_symbol_exprContext):
        s = ctx.str_().getText()
        return Automata()

    # Visit a parse tree produced by GramParser#sa_state.
    def visitSa_state(self, ctx: GramParser.Sa_stateContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GramParser#get_state.
    def visitGet_state(self, ctx: GramParser.Get_stateContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GramParser#int_expr.
    def visitInt_expr(self, ctx: GramParser.Int_exprContext):
        return int(ctx.int_().getText())

    # Visit a parse tree produced by GramParser#load_expr.
    def visitLoad_expr(self, ctx: GramParser.Load_exprContext):
        path = ctx.PATH().getText()
        return build_dfa_from_graph(get_graph(path))

    # Visit a parse tree produced by GramParser#add_state_expr.
    def visitAdd_state_expr(self, ctx: GramParser.Add_state_exprContext):
        expr: Automata = self.visit(ctx.expr()[0])
        states = self.visit(ctx.expr()[1])
        is_start = ctx.sa_state().getText() == 'start'
        if is_start:
            expr.start_states.update(states)
        else:
            expr.final_states.update(states)
        return expr


    # Visit a parse tree produced by GramParser#union_expr.
    def visitUnion_expr(self, ctx: GramParser.Union_exprContext):
        e1: Automata = self.visit(ctx.expr()[0])
        e2: Automata = self.visit(ctx.expr()[1])
        return e1.union(e2)

    # Visit a parse tree produced by GramParser#name_expr.
    def visitName_expr(self, ctx: GramParser.Name_exprContext):
        name = ctx.name().getText()
        if name not in self.env:
            raise 'No such var!'
        return self.env[name]

    # Visit a parse tree produced by GramParser#string_expr.
    def visitString_expr(self, ctx: GramParser.String_exprContext):
        return ctx.STRING().getText()

    # Visit a parse tree produced by GramParser#filter_expr.
    def visitFilter_expr(self, ctx: GramParser.Filter_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GramParser#assign_state_expr.
    def visitAssign_state_expr(self, ctx: GramParser.Assign_state_exprContext):
        expr: Automata = self.visit(ctx.expr()[0])
        states = self.visit(ctx.expr()[1])
        is_start = ctx.sa_state().getText() == 'start'
        if is_start:
            expr.start_states.clear()
            expr.start_states.update(states)
        else:
            expr.final_states.clear()
            expr.final_states.update(states)
        return expr


    # Visit a parse tree produced by GramParser#intersection_expr.
    def visitIntersection_expr(self, ctx: GramParser.Intersection_exprContext):
        e1: Automata = self.visit(ctx.expr()[0])
        e2: Automata = self.visit(ctx.expr()[1])
        return e1.get_intersection(e2)

    # Visit a parse tree produced by GramParser#brackets_expr.
    def visitBrackets_expr(self, ctx: GramParser.Brackets_exprContext):
        return self.visit(ctx.expr())

    # Visit a parse tree produced by GramParser#unistar_expr.
    def visitUnistar_expr(self, ctx: GramParser.Unistar_exprContext):
        e = self.visit(ctx.expr())

        if not isinstance(e, Automata):
            raise 'Invalid type!'

        return e.kleene_star()

    # Visit a parse tree produced by GramParser#bistar_expr.
    def visitBistar_expr(self, ctx: GramParser.Bistar_exprContext):
        e1: Automata = self.visit(ctx.expr()[0])
        e2: Automata = self.visit(ctx.expr()[1])
        return e1.kleene_star().concatenate(e2)

    # Visit a parse tree produced by GramParser#unequality_expr.
    def visitUnequality_expr(self, ctx: GramParser.Unequality_exprContext):
        e1: Automata = self.visit(ctx.expr()[0])
        e2: Automata = self.visit(ctx.expr()[1])
        return not e1.is_equivalent_to(e2)

    # Visit a parse tree produced by GramParser#map_expr.
    def visitMap_expr(self, ctx: GramParser.Map_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by GramParser#equality_expr.
    def visitEquality_expr(self, ctx: GramParser.Equality_exprContext):
        e1: Automata = self.visit(ctx.expr()[0])
        e2: Automata = self.visit(ctx.expr()[1])
        return e1.is_equivalent_to(e2)

    # Visit a parse tree produced by GramParser#concat_expr.
    def visitConcat_expr(self, ctx: GramParser.Concat_exprContext):
        e1: Automata = self.visit(ctx.expr()[0])
        e2: Automata = self.visit(ctx.expr()[1])
        return e1.concatenate(e2)

    # Visit a parse tree produced by GramParser#get_state_expr.
    def visitGet_state_expr(self, ctx: GramParser.Get_state_exprContext):
        state_type = ctx.get_state().getText()
        expr: Automata = self.visit(ctx.expr())
        if state_type == 'start':
            return expr.start_states
        elif state_type == 'final':
            return expr.final_states
        elif state_type == 'reachable':
            return expr._get_reachable_states()
        elif state_type == 'nodes':
            return expr.states
        elif state_type == 'edges':
            return expr._transition_function.get_edges()
        elif state_type == 'labels':
            return expr.symbols


def main():
    do('my_code.txt')


def do(path: str):
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
    output = visitor.visit(tree)


if __name__ == '__main__':
    main()
