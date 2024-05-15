from copy import copy
import functools
import itertools

import pyformlang as pl
from pyformlang.cfg import Variable, Terminal
import networkx as nx

LABEL = "label"


class FreshVar:
    var_counter = 0

    @classmethod
    def generate_fresh(cls, var: str) -> str:
        cls.var_counter += 1
        return f"{var}{cls.var_counter}"


class Program:
    EPS = '"a"^[0]'
    nonterminal_names = {}
    result_name = ""

    @staticmethod
    def _nonterminal_to_string(nonterminal: Variable) -> str:
        return nonterminal.to_text().lower()

    @staticmethod
    def _terminal_to_string(terminal: Terminal) -> str:
        terminal_s = terminal.to_text().lower()
        if len(terminal_s) == 1:
            return f'"{terminal_s}"'
        res = ""
        for key, group in itertools.groupby(terminal_s):
            dot = " . " if res != "" else ""
            res += f'{dot}"{key}"^[{len(group)}]'
        return res

    def __init__(
        self,
        graph: nx.MultiDiGraph,
        cfg: pl.cfg.CFG,
        start_nodes: set[int],
        final_nodes=None,
    ):
        self.graph = graph.copy()
        self.graph.name = (
            FreshVar.generate_fresh(graph.name)
            if graph.name != ""
            else FreshVar.generate_fresh("g")
        )
        self.grammar = copy(cfg)
        self.start_nodes = start_nodes
        self.final_nodes = final_nodes
        self.result_name = FreshVar.generate_fresh("r")
        for production in cfg.productions:
            if production.head not in self.nonterminal_names.keys():
                self.nonterminal_names[production.head] = FreshVar.generate_fresh(
                    self._nonterminal_to_string(production.head)
                )

    def _graph_to_program(self) -> str:
        program = f"let {self.graph.name} is graph"
        for node_from, node_to, data in self.graph.edges(data=True):
            program += f'\nadd edge ({node_from}, "{data[LABEL]}", {node_to}) to {self.graph.name}'
        return program

    def _object_to_string(self, cfg_object: Variable | Terminal) -> str:
        if isinstance(cfg_object, Variable):
            return self.nonterminal_names[cfg_object]
        return self._terminal_to_string(cfg_object)

    def _objs_to_expr(self, objects: list[pl.cfg.production.CFGObject]) -> str:
        if len(objects) == 0:
            return self.EPS
        return functools.reduce(
            lambda acc, obj: f"{acc}{' . ' if acc != '' else ''}{self._object_to_string(obj)}",
            objects,
            "",
        )

    def _objs_alts(self, objects: list[list[pl.cfg.production.CFGObject]]) -> str:
        return functools.reduce(
            lambda acc, objs: f"{acc}{' | ' if acc != '' else ''}{self._objs_to_expr(objs)}",
            objects,
            "",
        )

    def _cfg_to_program(self) -> str:
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

    def _query_to_program(self) -> str:
        query_name = self.nonterminal_names[self.grammar.start_symbol]
        start_set_expr = (
            "["
            + functools.reduce(
                lambda acc, x: f"{acc}{', ' if acc != '' else ''}{str(x)}",
                self.start_nodes,
                "",
            )
            + "]"
        )
        if len(self.final_nodes) == 0:
            return f"\nlet {self.result_name} = for v in {start_set_expr} return u, v where u reachable from v in {self.graph.name} by {query_name}"
        final_set_expr = (
            "["
            + functools.reduce(
                lambda acc, x: f"{acc}{', ' if acc != '' else ''}{str(x)}",
                self.final_nodes,
                "",
            )
            + "]"
        )
        return (
            f"\nlet {self.result_name} = for v in {start_set_expr} for u in {final_set_expr} return u, v where u reachable from v in {self.graph.name} "
            f"by {query_name}"
        )

    def __str__(self):
        program = ""
        program += self._graph_to_program()
        cfg_pr = self._cfg_to_program()
        program += cfg_pr
        program += self._query_to_program()
        return program


WELL_TYPED = [
    """
    let p = "a" . p . "b" | "c"
    let q = ("s" . "f") ^ [1..]
    let g = q & p""",
    """
    let p = "a" . "b" | "c"
    let q = ("s" . "f") ^ [1..]
    let g = [q, p]
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
