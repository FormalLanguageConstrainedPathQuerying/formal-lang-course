from copy import copy, deepcopy

import pyformlang as pl
from pyformlang.cfg import Variable, Terminal
import networkx as nx
from constants import LABEL


class FreshVar:
    var_counter = 0

    @classmethod
    def generate_fresh(cls, var: str) -> str:
        cls.var_counter += 1
        return f"{var}{cls.var_counter}"


def _nonterminal_to_string(nonterminal: Variable) -> str:
    return nonterminal.to_text().lower()


def _terminal_to_string(terminal: Terminal) -> str:
    """
    convert terminal symbol into char
    :param terminal: terminal symbol
    :return: an object view of "x"
    """
    terminal_s = terminal.to_text().lower()
    return f'"{terminal_s}"'


class GraphProgram:
    def __init__(self, graph: nx.MultiDiGraph):
        self.graph = graph.copy()
        self.name = (
            FreshVar.generate_fresh(graph.name)
            if graph.name != ""
            else FreshVar.generate_fresh("g")
        )

    def __str__(self):
        program = f"\nlet {self.name} is graph"
        for node_from, node_to, data in self.graph.edges(data=True):
            program += (
                f'\nadd edge ({node_from}, "{data[LABEL]}", {node_to}) to {self.name}'
            )
        return program


class GrammarProgram:
    EPS = '"a"^[0 .. 0]'

    def __init__(self, cfg: pl.cfg.CFG):
        self.grammar = copy(cfg)
        self.nonterminal_names = {}
        for production in cfg.productions:
            if production.head not in self.nonterminal_names.keys():
                self.nonterminal_names[production.head] = FreshVar.generate_fresh(
                    _nonterminal_to_string(deepcopy(production.head))
                )
        self.start_nonterminal_name = self.nonterminal_names[cfg.start_symbol]

    def _object_to_string(self, cfg_object: Variable | Terminal) -> str:
        """
        convert nonterminal or terminal symbol into program representation
        :param cfg_object: terminal or nonterminal
        :return: an object view of "x", if object is terminal or x, if object is nonterminal
        """
        if isinstance(cfg_object, Variable):
            return self.nonterminal_names[cfg_object]
        return _terminal_to_string(cfg_object)

    def _objs_to_expr(self, objects: list[pl.cfg.production.CFGObject]) -> str:
        if len(objects) == 0:
            return self.EPS
        return " . ".join(map(self._object_to_string, objects))

    def _objs_alts(self, objects: list[list[pl.cfg.production.CFGObject]]) -> str:
        return " | ".join(map(self._objs_to_expr, objects))

    def __str__(self) -> str:
        res = ""
        vars_dict: dict[pl.cfg.Variable, list[list[pl.cfg.production.CFGObject]]] = {}
        for production in self.grammar.productions:
            head = production.head
            body = production.body
            if head in vars_dict.keys():
                vars_dict[head].append(body)
            else:
                vars_dict[head] = [body]
        for nonterminal in vars_dict.keys():
            res += f"\nlet {self.nonterminal_names[nonterminal]} = {self._objs_alts(vars_dict[nonterminal])}"
        return res


class QueryProgram:
    def __init__(
        self,
        graph_program: GraphProgram,
        grammar_program: GrammarProgram,
        start_nodes: set[int],
        final_nodes: set[int] = None,
    ):
        if final_nodes is None:
            final_nodes = set()
        self.graph_program = graph_program
        self.grammar_program = grammar_program
        self.result_name = FreshVar.generate_fresh("r")
        self.start_nodes = start_nodes
        self.final_nodes = final_nodes

    def get_graph(self):
        return self.graph_program.graph

    def get_grammar(self):
        return self.grammar_program.grammar

    def query_program(self) -> str:
        """
        if you want only want to get query
        :return: just select expression
        """
        query_name = self.grammar_program.start_nonterminal_name
        start_set_expr = f"[{', '.join(map(str, self.start_nodes))}]"
        if len(self.final_nodes) == 0:
            return (
                f"\nlet {self.result_name} = for v in {start_set_expr} return u, v where u reachable from v in "
                f"{self.graph_program.name} by {query_name}"
            )
        final_set_expr = f"[{', '.join(map(str, self.final_nodes))}]"
        return (
            f"\nlet {self.result_name} = for v in {start_set_expr} for u in {final_set_expr} return u, v where u "
            f"reachable from v in {self.graph_program.name} by {query_name}"
        )

    def full_program(self) -> str:
        """
        if you want to work with query as meaningful object
        :return: fully query with predefined graph and grammar
        """
        return f"\n{self.graph_program}\n{self.grammar_program}\n{self.query_program()}"


def to_program_parser(
    query_list: list[QueryProgram],
) -> tuple[str, dict[str, QueryProgram]]:
    result_program = ""
    res_name_query = {}
    grammar_set = set()
    graph_set = set()
    for query in query_list:
        # if graph is already defined then it is not necessary to define it again
        if query.graph_program not in graph_set:
            result_program += str(query.graph_program)
            graph_set.add(query.graph_program)
        # same with grammar
        if query.grammar_program not in grammar_set:
            result_program += str(query.grammar_program)
            grammar_set.add(query.grammar_program)
        result_program += query.query_program()
        res_name_query.update({query.result_name: query})
    return result_program, res_name_query


WELL_TYPED = [
    """
    let p = "a" . p . "b" | "c"
    let q = ("s" . "f") ^ [1..]
    let g = q & p""",
    """
    let a = ("a" . b) | "a" ^ [0]
    let b = a . "b"
    """,
    """
    let q = "a" . p
    let p = "b" . r
    let r = ("c" . r) | "c" ^ [0]
    """,
    """
    let p = (1,"a",2)
    let g is graph
    remove edge p from g
    """,
    """
    let p = 1
    let g is graph
    remove vertex p from g
    """,
    """
    let p = [1,2]
    let g is graph
    remove vertices p from g
    """,
    """
    let p = "a" . p . "b" | "c"
    let g is graph
    let r1 =
        return v
        where u reachable from v in g by p
    let q = "s" . q . "f" | "e"
    let r2 =
        for v in r1
        return u,v
        where u reachable from v in g by q
    """,
    """
    let p = "a" . p . "b" | "c"
    let g is graph
    remove vertices
        return v
        where u reachable from v in g by p
    from g
    """,
    """
    let p = "a" . p . "b" | "c"
    let g is graph
    let q = "c" ^ [1..]
    let r =
        for v in
            return v
            where u reachable from v in g by p
        return u,v
        where v reachable from u in g by q
    """,
]

ILL_TYPED = [
    """
    let p = "a" . p . "b" | "c"
    let q = "s" . q . "f" | "e"
    let g = q & p
    """,
    """
    let p = "a" . p . "b" | "c"
    let q = ("s" . "f") ^ [1..]
    let g = [q, p]
    """,
    """
    let p = "a" . "b" | "c"
    let q = ("s" . "f") ^ [1..]
    let g = [q, p]
    """,
    """
    let p = "a" . p . "b" | "c"
    let g is graph
    let r1 =
        return u,v
        where u reachable from v in g by p
    let q = "s" . q . "f" | "e"
    let r2 =
        for v in r1
        return u,v
        where u reachable from v in g by q
    """,
    """
    let p = "a" . p . "b" | "c"
    let g is graph
    remove edge p from g
    """,
    """
    let p = (1,"a",2)
    let g is graph
    remove vertex p from g
    """,
    """
    let p = 1
    let g is graph
    remove vertices p from g
    """,
    """
    let p = 1
    let g is graph
    let x =
        return v
        where v reachable from u in g by p
    """,
]
