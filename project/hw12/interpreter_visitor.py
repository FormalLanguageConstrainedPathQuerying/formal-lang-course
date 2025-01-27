from project.hw11.GLparserVisitor import GLparserVisitor
from networkx import MultiDiGraph
from pyformlang.finite_automaton import EpsilonNFA
from project.hw12.automata_utils import (
    nfa_from_char,
    nfa_from_var,
    group,
    intersect,
    concatenate,
    union,
    repeat_range,
    build_rsm,
)
from project.hw8.tensor_based_cfpq import tensor_based_cfpq


def extract_var_name(ctx):
    return str(ctx.VAR().getText())


class InterpreterVisitor(GLparserVisitor):
    def __init__(self):
        super().__init__()
        self._vars = {}
        self._query_output = {}
        self._query_done = False

    @property
    def last_query_results(self):
        return dict(self._query_output)

    def visitProg(self, ctx):
        return self.visitChildren(ctx)

    def visitStmt(self, ctx):
        return self.visitChildren(ctx)

    def visitDeclare(self, ctx):
        name = extract_var_name(ctx.var_p())
        self._vars[name] = MultiDiGraph()

    def visitBind(self, ctx):
        name = extract_var_name(ctx.var_p())
        val = self.visitExpr(ctx.expr())

        if isinstance(val, str) and len(val) == 1:
            val = nfa_from_char(val)

        self._vars[name] = val

        if self._query_done:
            self._query_done = False
            self._query_output[name] = val

    def visitExpr(self, ctx):
        return self.visitChildren(ctx)

    def visitRegexp(self, ctx):
        has_brackets = bool(ctx.LPAREN() and ctx.RPAREN())

        if ctx.char_p():
            return nfa_from_char(self.visitChar_p(ctx.char_p()))
        if ctx.var_p():
            return nfa_from_var(ctx.var_p().getText())
        if has_brackets:
            return group(self.visitRegexp(ctx.regexp(0)))

        if ctx.PATDENY():
            left, range_ = (
                self.visitRegexp(ctx.regexp(0)),
                self.visitRange(ctx.range_()),
            )
            return repeat_range(
                left, self.visitNum_p(range_[0]), self.visitNum_p(range_[1])
            )

        left = self.visitRegexp(ctx.regexp(0))
        right = self.visitRegexp(ctx.regexp(1))

        if ctx.ALTERNATIVE():
            return union(left, right)
        if ctx.WILDCARD():
            return concatenate(left, right)
        if ctx.REGAND():
            return intersect(left, right)

    def visitSelect(self, ctx):
        filter1 = self.visitV_filter(ctx.v_filter(0))
        filter2 = self.visitV_filter(ctx.v_filter(1))

        var_list = ctx.var_p()
        graph = self.visitVar_p(var_list[-1])

        nfa_dict = {k: v for k, v in self._vars.items() if isinstance(v, EpsilonNFA)}
        query = build_rsm(self._nfa_from_expr(ctx.expr()), nfa_dict)

        start_var = extract_var_name(var_list[-2])
        final_var = extract_var_name(var_list[-3])

        start_nodes = filter1[1] if start_var == filter1[0] else filter2[1]
        final_nodes = filter2[1] if final_var == filter2[0] else filter1[1]

        result = tensor_based_cfpq(query, graph, start_nodes, final_nodes)

        ret_var1 = var_list[0].getText()
        ret_var2 = var_list[1].getText() if len(var_list) > 1 else None
        start_name = var_list[-2].getText()
        final_name = var_list[-3].getText()

        if ret_var1 == start_name and not ret_var2:
            output = {r[0] for r in result}
        elif ret_var1 == final_name and not ret_var2:
            output = {r[1] for r in result}
        else:
            output = result

        self._query_done = True
        return output

    def visitV_filter(self, ctx):
        if not ctx:
            return None, None
        return ctx.var_p().getText(), self.visitExpr(ctx.expr())

    def visitAdd(self, ctx):
        graph = self.visitVar_p(ctx.var_p())
        expr_val = self.visitExpr(ctx.expr())

        if ctx.EDGE():
            graph.add_edge(expr_val[0], expr_val[2], label=expr_val[1])
        else:
            graph.add_node(expr_val)

    def visitRemove(self, ctx):
        graph = self.visitVar_p(ctx.var_p())
        expr_val = self.visitExpr(ctx.expr())

        if ctx.EDGE():
            graph.remove_edge(expr_val[0], expr_val[2])
        elif ctx.VERTEX():
            graph.remove_node(expr_val)
        else:
            [graph.remove_node(v) for v in expr_val]

    def visitSet_expr(self, ctx):
        return {self.visitExpr(expr) for expr in ctx.expr()}

    def visitEdge_expr(self, ctx):
        exprs = ctx.expr()
        return (
            self.visitExpr(exprs[0]),
            self.visitExpr(exprs[1]),
            self.visitExpr(exprs[2]),
        )

    def visitRange(self, ctx):
        return ctx.num_p(0), ctx.num_p(1)

    def visitNum_p(self, ctx):
        return int(ctx.NUM().getText())

    def visitChar_p(self, ctx):
        return str(ctx.CHAR().getText()[1])

    def _nfa_from_expr(self, ctx):
        val = self.visitExpr(ctx)
        if isinstance(val, EpsilonNFA):
            return val
        if isinstance(val, str):
            return nfa_from_char(val)
        raise Exception(f"Cannot convert '{val}' to EpsilonNFA")

    def visitVar_p(self, ctx):
        name = extract_var_name(ctx)
        if name not in self._vars:
            raise Exception(f"Variable '{name}' doesn't exist")
        return self._vars[name]
