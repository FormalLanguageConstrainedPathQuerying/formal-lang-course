from pathlib import Path
from networkx import MultiDiGraph
from pyformlang.cfg import CFG
from pyformlang.cfg import Variable
from pyformlang.cfg import Terminal
from project.grammar import cfg_to_weak_cnf, cfg_from_file
from project.graph_utils import GraphUtils


def hellings(cfg: CFG, graph: MultiDiGraph) -> set[tuple[object, Variable, object]]:
    eps_productions = set()
    terminal_productions: dict[Variable, set] = {}
    non_terminal_productions: dict[Variable, set[tuple]] = {}
    for p in cfg_to_weak_cnf(cfg).productions:
        body = p.body
        if len(body) == 0:
            eps_productions.add(p.head)
        elif len(body) == 1:
            terminal_productions.setdefault(p.head, set()).add(body[0])
        elif len(body) == 2:
            u, v = body
            non_terminal_productions.setdefault(p.head, set()).add((u, v))

    res = {(n, v, n) for n in graph.nodes for v in eps_productions}
    for A, B, label in graph.edges.data("label"):
        for key, value in terminal_productions.items():
            if Terminal(label) in value:
                res.add((A, key, B))

    queue = res.copy()
    while queue:
        begin_a, u, end_a = queue.pop()
        buf = set()
        for begin_b, v, end_b in res:
            if end_a == begin_b:
                for w in non_terminal_productions:
                    if (u, v) in non_terminal_productions[w] and (
                        begin_a,
                        w,
                        end_b,
                    ) not in res:
                        queue.add((begin_a, w, end_b))
                        buf.add((begin_a, w, end_b))
            if end_b == begin_a:
                for w in non_terminal_productions:
                    if (v, u) in non_terminal_productions[w] and (
                        begin_b,
                        w,
                        end_a,
                    ) not in res:
                        queue.add((begin_b, w, end_a))
                        buf.add((begin_b, w, end_a))
        res |= buf

    return res


def hellings_graph_from_file(
    graph_filename: Path, cfg: CFG
) -> set[tuple[object, Variable, object]]:
    return hellings(cfg, GraphUtils.open_graph(graph_filename))


def hellings_cfg_from_text(
    graph: MultiDiGraph, cfg_text: str, start_symbol=Variable("S")
) -> set[tuple[object, Variable, object]]:
    return hellings(CFG.from_text(cfg_text, start_symbol=start_symbol), graph)


def hellings_cfg_from_file(
    graph: MultiDiGraph, cfg_filename: str, start_symbol="S"
) -> set[tuple[object, Variable, object]]:
    return hellings(cfg_from_file(cfg_filename, start_symbol), graph)


def hellings_cfg_and_graph_from_file(
    graph_filename: Path, cfg_filename: str, start_symbol="S"
) -> set[tuple[object, Variable, object]]:
    return hellings_cfg_from_file(
        GraphUtils.open_graph(graph_filename), cfg_filename, start_symbol
    )
