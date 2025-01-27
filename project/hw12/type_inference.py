from project.hw12.type_utils import Env
from project.hw12.types_t import Types_t
from project.hw11.GLparserVisitor import GLparserVisitor


def _check_type(expected: Types_t, actual: Types_t, context: str) -> None:
    if expected != actual:
        raise Exception(f"Type mismatch in {context}: expected {expected}, got {actual}")


class GLTypesInferencer(GLparserVisitor):
    def __init__(self):
        super().__init__()
        self._env = Env()

    def _validate_var_exists(self, var_name: str) -> None:
        if not self._env.contain_variable(var_name):
            raise Exception(f"Variable '{var_name}' doesn't exist")

    def _validate_var_not_exists(self, var_name: str, context: str) -> None:
        if self._env.contain_variable(var_name):
            raise Exception(f"Variable '{var_name}' already exists in {context}")

    def visitProg(self, ctx):
        return self.visitChildren(ctx)

    def visitStmt(self, ctx):
        return self.visitChildren(ctx)

    def visitDeclare(self, ctx):
        var_name = ctx.var_p().VAR().getText()
        self._env.add_variable(var_name, Types_t.GRAPH)

    def visitAdd(self, ctx):
        var_name = ctx.var_p().VAR().getText()
        var_type = self.visitVar_p(ctx.var_p())
        _check_type(Types_t.GRAPH, var_type, f"Variable '{var_name}'")

        entity_type = self.visitExpr(ctx.expr())

        if ctx.EDGE():
            _check_type(Types_t.EDGE, entity_type, "Edge construction")
        elif ctx.VERTEX():
            _check_type(Types_t.NUM, entity_type, "Vertex construction")

    def visitRemove(self, ctx):
        var_name = ctx.var_p().VAR().getText()
        var_type = self.visitVar_p(ctx.var_p())
        _check_type(Types_t.GRAPH, var_type, f"Variable '{var_name}'")

        entity_type = self.visitExpr(ctx.expr())

        if ctx.EDGE():
            _check_type(Types_t.EDGE, entity_type, "Edge removal")
        elif ctx.VERTEX():
            _check_type(Types_t.NUM, entity_type, "Vertex removal")
        elif ctx.VERTICES():
            _check_type(Types_t.SET, entity_type, "Vertices removal")

    def visitBind(self, ctx):
        var_name = ctx.var_p().VAR().getText()
        expr_type = self.visitExpr(ctx.expr())
        self._env.add_variable(var_name, expr_type)

    def visitExpr(self, ctx):
        return self.visitChildren(ctx)

    def visitRegexp(self, ctx):
        if ctx.char_p():
            return Types_t.FA

        if ctx.var_p():
            var_name = ctx.var_p().VAR().getText()
            if not self._env.contain_variable(var_name):
                return Types_t.RSM

            var_type = self.visitVar_p(ctx.var_p())
            if var_type in [Types_t.FA, Types_t.CHAR]:
                return Types_t.FA
            if var_type == Types_t.RSM:
                return Types_t.RSM
            raise Exception(f"Invalid type {var_type} for regexp variable {var_name}")

        if ctx.LPAREN() and ctx.RPAREN():
            return self.visitRegexp(ctx.regexp(0))

        if ctx.PATDENY():
            left_type = self.visitRegexp(ctx.regexp(0))
            range_type = self.visitRange(ctx.range_())
            _check_type(Types_t.RANGE, range_type, "Range expression")

            if left_type not in [Types_t.FA, Types_t.RSM]:
                raise Exception(f"Invalid type {left_type} for repeat operation")
            return left_type

        left_type = self.visitRegexp(ctx.regexp(0))
        right_type = self.visitRegexp(ctx.regexp(1))

        if ctx.ALTERNATIVE() or ctx.WILDCARD():
            return Types_t.RSM if Types_t.RSM in [left_type, right_type] else Types_t.FA

        if ctx.REGAND():
            if left_type == Types_t.RSM and right_type == Types_t.RSM:
                raise Exception("Cannot intersect two RSMs")
            return Types_t.RSM if Types_t.RSM in [left_type, right_type] else Types_t.FA

        return Types_t.UNKNOWN

    def visitSelect(self, ctx):
        self.visitV_filter(ctx.v_filter(0))
        self.visitV_filter(ctx.v_filter(1))

        vars = ctx.var_p()
        in_var = vars[-1].VAR().getText()
        from_var = vars[-2].VAR().getText()
        where_var = vars[-3].VAR().getText()

        _check_type(Types_t.GRAPH, self._env.get_variable(in_var), f"Variable {in_var}")

        result_var1 = vars[0].VAR().getText()
        result_var2 = vars[1].VAR().getText() if ctx.COMMA() else None

        if result_var1 not in [where_var, from_var]:
            raise Exception(f"Result variable must be {from_var} or {where_var}")
        if result_var2 and result_var2 not in [where_var, from_var]:
            raise Exception(f"Second result variable must be {from_var} or {where_var}")

        expr_type = self.visitExpr(ctx.expr())
        if expr_type not in [Types_t.FA, Types_t.RSM, Types_t.CHAR]:
            raise Exception(f"Invalid expression type {expr_type} in SELECT")

        return Types_t.PAIR_SET if result_var2 else Types_t.SET

    def visitV_filter(self, ctx):
        if not ctx:
            return None

        var_name = ctx.var_p().VAR().getText()
        self._validate_var_not_exists(var_name, "FOR context")

        expr_type = self.visitExpr(ctx.expr())
        _check_type(Types_t.SET, expr_type, "Filter expression")

        return var_name

    def visitSet_expr(self, ctx):
        for expr in ctx.expr():
            _check_type(Types_t.NUM, self.visitExpr(expr), "Set element")
        return Types_t.SET

    def visitEdge_expr(self, ctx):
        exprs = ctx.expr()
        types = [self.visitExpr(e) for e in exprs]

        if (types[0] == Types_t.NUM and
                types[1] == Types_t.CHAR and
                types[2] == Types_t.NUM):
            return Types_t.EDGE

        raise Exception(f"Invalid edge construction: {ctx.getText()}")

    def visitRange(self, ctx):
        return Types_t.RANGE

    def visitNum_p(self, ctx):
        return Types_t.NUM

    def visitChar_p(self, ctx):
        return Types_t.CHAR

    def visitVar_p(self, ctx):
        var_name = ctx.VAR().getText()
        self._validate_var_exists(var_name)
        return self._env.get_variable(var_name)