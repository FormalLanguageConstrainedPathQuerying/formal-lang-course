from antlr4 import ParserRuleContext
from project.hw11.GLparserParser import GLparserParser
from project.hw11.GLparserVisitor import GLparserVisitor
from project.hw2.regex_to_dfa_tool import regex_to_dfa

class InterpreterVisitor(GLparserVisitor):
        def __init__(self):
            self.env = [{}]

        def set_var(self, var: str, value):
            self.env[-1][var] = value
        def get_var(self, var_name:str):
            for env in self.env:
                if var_name in env:
                    return env[var_name]
            raise Exception('Variable "{}" not found'.format(var_name))

        def add_env(self, env: dict):
            self.env.append(env)

        def pop_env(self):
            if len(self.env) < 2:
                raise RuntimeError("You try to pop an global environment")
            self.env.pop()

        def visitProg(self, ctx: ParserRuleContext):
            return self.visitChildren(ctx)

        def visitBind(self, ctx: GLparserParser.BindContext):
            var_name = ctx.VAR().getText()
            value = self.visitChildren(ctx)
            self.set_var(var_name, value)

        def visitExpr(self, ctx: GLparserParser.ExprContext):
            regexp = self.visitChildren(ctx)
            return regexp

        def visitRegexp(self, ctx: GLparserParser.RegexpContext):
            # tst = self.visitChildren(ctx)
            if ctx.getChildCount() == 3:
                op = ctx.getChild(1).getText()
                if op == '|':
                    left_regex = self.visit(ctx.getChild(0))
                    right_regex = self.visit(ctx.getChild(2))
                    return f"{left_regex} {op} {right_regex}"
                elif op == '^':
                    left_regex = self.visit(ctx.getChild(0))
                    right_regex = self.visit(ctx.getChild(2))
                    res_reg = ""
                    for el in range(int(right_regex[0]), int(right_regex[1]) + 1):
                        if el < int(right_regex[1]):
                            res_reg = res_reg + ("(" + left_regex + ")") * el + "|"
                        else:
                            res_reg = res_reg + ("(" + left_regex + ")") * el
                    return f"{res_reg}"
            if ctx.getChildCount() == 1:
                return ctx.getChild(0).getText()
        def visitRange(self, ctx:GLparserParser.RangeContext):
            num_1 = ctx.getChild(1).getText()
            num_2 = ctx.getChild(3).getText()
            return(num_1, num_2)

        # def visitTerminal(self, node):
        #      return node


            # return 1
            # return ctx.VAR().getText()


        # def visitDeclare(self, ctx:GLparserParser.DeclareContext):
        #     declare_name = ctx.VAR().getText()
        #     self.set_var(declare_name, "")
        #
        # def visitVar(self, ctx):
        #     return self.get_var(ctx.VAR().getText())

        # def visitRange(self, ctx:GLparserParser.RangeContext):
        #     a = ctx.NUM(1).getText()
        #     b = ctx.NUM(2).getText()
        #     TODO

        # def gen_repeat_grammar_from_

        # def visitRegexp(self, ctx:GLparserParser.RegexpContext):
        #     try:
        #         regexp = tree_to_program(ctx)
        #         reg_dfa = regex_to_dfa(regexp)
        #         return reg_dfa
        #     except Exception as e:


        # def visitAlternative(self, ctx):
        #     left_regexp = self.visit(ctx.getChild(0))
        #     right_regexp = self.visit(ctx.getChild(1))


        # def visitRegex(self, contex: GLparserParser.RegexpContext):
        #     return LFiniteAutoma.from_string(contex.REGEX().getText()[2:-1])
        # def visitVar(self, ctx: GLparserParser.Con):
        #     var_name = ctx.VAR().getText()
        #     return self.get_var(var_name)

    # def visitInt(self, contex: LenguageParser.IntContext):
    #     return int(contex.INT().getText())
    #
    # def visitString(self, contex: LenguageParser.StringContext):
    #     return contex.STRING().getText()[1:-1]


# class Type(Enum):
#     FA = auto()
#     RSM = auto()
#     CHAR = auto()
#     SET = auto()
#     GRAPH = auto()
#
#
# @dataclass
# class Environment:
#     bindings: Dict[str, Tuple[Type, object]] = None
#
#     def __post_init__(self):
#         if self.bindings is None:
#             self.bindings = {}
#
#     def bind(self, name: str, type_: Type, value: object):
#         self.bindings[name] = (type_, value)
#
#     def get(self, name: str) -> Tuple[Type, object]:
#         return self.bindings.get(name)
#
#
# class GLInterpreter(GLparserVisitor):
#     def __init__(self):
#         self.env = Environment()
#         self.query_results = {}
#
#     def visitProg(self, ctx: GLparserParser.ProgContext):
#         for stmt in ctx.stmt():
#             self.visit(stmt)
#         return self.query_results
#
#     def visitDeclare(self, ctx: GLparserParser.DeclareContext):
#         var_name = ctx.VAR().getText()
#         self.env.bind(var_name, Type.GRAPH, set())
#
#     def visitBind(self, ctx: GLparserParser.BindContext):
#         var_name = ctx.VAR().getText()
#         expr_type, expr_value = self.visit(ctx.expr())
#         self.env.bind(var_name, expr_type, expr_value)
#         if isinstance(ctx.expr(), GLparserParser.SelectContext):
#             self.query_results[var_name] = expr_value
#
#     def visitEdge_expr(self, ctx: GLparserParser.Edge_exprContext):
#         src_type, src_val = self.visit(ctx.expr(0))
#         label_type, label_val = self.visit(ctx.expr(1))
#         dst_type, dst_val = self.visit(ctx.expr(2))
#         return (Type.FA, (src_val, label_val, dst_val))
#
#     def visitSet_expr(self, ctx: GLparserParser.Set_exprContext):
#         values = set()
#         for expr in ctx.expr():
#             _, val = self.visit(expr)
#             values.add(val)
#         return (Type.SET, values)
#
#     def visitRegexp(self, ctx: GLparserParser.RegexpContext):
#         if ctx.CHAR():
#             return (Type.CHAR, ctx.CHAR().getText().strip('"'))
#         elif ctx.VAR():
#             return self.env.get(ctx.VAR().getText())
#         elif ctx.REGAND():
#             left_type, left_val = self.visit(ctx.regexp(0))
#             right_type, right_val = self.visit(ctx.regexp(1))
#             if left_type == Type.FA and right_type == Type.FA:
#                 return (Type.FA, f"({left_val}&{right_val})")
#             return (Type.RSM, f"({left_val}&{right_val})")
#         elif ctx.ALTERNATIVE():
#             left_type, left_val = self.visit(ctx.regexp(0))
#             right_type, right_val = self.visit(ctx.regexp(1))
#             if left_type == Type.FA and right_type == Type.FA:
#                 return (Type.FA, f"({left_val}|{right_val})")
#             return (Type.RSM, f"({left_val}|{right_val})")
#         elif ctx.WILDCARD():
#             return (Type.FA, ".*")
#         elif ctx.PATDENY():
#             expr_type, expr_val = self.visit(ctx.regexp(0))
#             range_val = self.visit(ctx.range())
#             return (expr_type, f"({expr_val}^{range_val})")
#
#     def visitSelect(self, ctx: GLparserParser.SelectContext):
#         pattern_type, pattern_val = self.visit(ctx.expr())
#         ret_vars = [ctx.VAR(0).getText()]
#         if ctx.VAR(1):
#             ret_vars.append(ctx.VAR(1).getText())
#
#         v_filters = []
#         if ctx.v_filter():
#             v_filters = [self.visit(f) for f in ctx.v_filter()]
#
#         if len(ret_vars) == 2:
#             return (Type.SET, set())  # Set of pairs
#         return (Type.SET, set())  # Set of single values
#
#     def visitV_filter(self, ctx: GLparserParser.V_filterContext):
#         var_name = ctx.VAR().getText()
#         expr_type, expr_val = self.visit(ctx.expr())
#         return var_name, expr_type, expr_val
#
#     def visitNUM(self, ctx: GLparserParser.Context):
#         return (Type.FA, int(ctx.getText()))
#
#     def visitCHAR(self, ctx: GLparserParser.CHARContext):
#         return (Type.CHAR, ctx.getText().strip('"'))
#
#     def visitVAR(self, ctx: GLparserParser.VARContext):
#         return self.env.get(ctx.getText())


