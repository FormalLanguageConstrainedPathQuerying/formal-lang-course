from project.cf_graph_recognizer import matrix_based, hellings, tensor
import networkx as nx
import pyformlang.cfg as c


def _cfpq(
    graph: nx.Graph,
    query: str | c.CFG,
    start_nodes: set[int] | None,
    final_nodes: set[int] | None,
    start_var: str | c.Variable,
    get_constrained_transitive_closure=hellings,
):
    if not isinstance(start_var, c.Variable):
        start_var = c.Variable(start_var)
    if not isinstance(query, c.CFG):
        query = c.CFG.from_text(query, start_symbol=start_var)
    if start_nodes is None:
        start_nodes = graph.nodes
    if final_nodes is None:
        final_nodes = graph.nodes
    if start_var is None:
        start_var = query.start_symbol

    constrained_transitive_closure = get_constrained_transitive_closure(graph, query)

    return {
        (start, var, final)
        for start, var, final in constrained_transitive_closure
        if start in start_nodes and var == start_var and final in final_nodes
    }


def hellings_cfpq(
    graph: nx.Graph,
    query: str | c.CFG,
    start_nodes: set[int] | None = None,
    final_nodes: set[int] | None = None,
    start_var: str | c.Variable = c.Variable("S"),
) -> set[tuple[int, int]]:
    return _cfpq(
        graph,
        query,
        start_nodes,
        final_nodes,
        start_var,
        hellings,
    )


def matrix_cfpq(
    graph: nx.Graph,
    query: str | c.CFG,
    start_nodes: set[int] | None = None,
    final_nodes: set[int] | None = None,
    start_var: str | c.Variable = c.Variable("S"),
) -> set[tuple[int, int]]:
    return _cfpq(
        graph,
        query,
        start_nodes,
        final_nodes,
        start_var,
        matrix_based,
    )


def tensor_cfpq(
    graph: nx.Graph,
    query: str | c.CFG,
    start_nodes: set[int] | None = None,
    final_nodes: set[int] | None = None,
    start_var: str | c.Variable = c.Variable("S"),
) -> set[tuple[int, int]]:
    return _cfpq(graph, query, start_nodes, final_nodes, start_var, tensor)
