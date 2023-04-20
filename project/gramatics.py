from typing import Union

import pydot
from networkx import MultiDiGraph, drawing
from pyformlang.cfg import CFG, Variable


def convert_to_weak_form(cfg: CFG) -> CFG:
    """
    Converts CFG to weak form CFG
    :param cfg:
    :return: CFG
    """
    cleared_cfg = cfg.eliminate_unit_productions().remove_useless_symbols()
    weak_cfg = cleared_cfg._get_productions_with_only_single_terminals()
    weak_cfg = cleared_cfg._decompose_productions(weak_cfg)
    return CFG(start_symbol=cleared_cfg.start_symbol, productions=set(weak_cfg))


def query_graph_with_cfg(
    graph: MultiDiGraph,
    cfg: Union[CFG, str],
    sn: set = None,
    fn: set = None,
    start_symbol: Variable = Variable("S"),
):
    """
    Constructs query graph with cfg
    :param graph: MultiFoGraph graph
    :param cfg: Union[CFG, str] cfg
    :param sn: set of start nodes
    :param fn: set of final nodes
    :param start_symbol: Variable start symbol
    :return: reachable pairs of vertices
    """
    sn = graph.nodes if sn is None else sn
    fn = graph.nodes if fn is None else fn

    return {
        (u, v)
        for (variable, u, v) in hellings_algorithm(graph, cfg)
        if variable == start_symbol and u in sn and v in fn
    }


def hellings_algorithm(graph: Union[MultiDiGraph, str], cfg: Union[CFG, str]):
    """
    Gets reachable pairs of vertex with help of hellings algorithm
    :param graph: Union[MultiDoGraph, str] graph
    :param cfg: Union[CFG, str] cfg
    :return: set of tuples
    """
    if isinstance(graph, str):
        graph = drawing.nx_pydot.from_pydot(pydot.graph_from_dot_data(graph)[0])
    if isinstance(cfg, str):
        cfg = CFG.from_text(cfg)

    cfg = convert_to_weak_form(cfg)

    result = set()
    variables_prod = set()
    for prod in cfg.productions:
        if len(prod.body) == 1:
            for (v, u, label) in graph.edges(data="label"):
                if label == prod.body[0].value:
                    result.add((prod.head, v, u))
        elif len(prod.body) != 2:
            for n in graph.nodes:
                result.add((prod.head, n, n))
        else:
            variables_prod.add(prod)

    queue = list(result)

    while len(queue) > 0:
        (var1, v, u) = queue.pop()
        to_append = set()
        for var2, v1, u1 in result:
            if v == u1 or u == v1:
                for prod in variables_prod:
                    if v == u1:
                        closure = (prod.head, v1, u)
                        if prod.body[0] == var2 and prod.body[1] == var1 and closure not in result:
                            to_append.add(closure)
                            queue.append(closure)
                    if u == v1:
                        closure = (prod.head, v, u1)
                        if prod.body[0] == var1 and prod.body[1] == var2 and closure not in result:
                            to_append.add(closure)
                            queue.append(closure)

        result = result.union(to_append)
    return result