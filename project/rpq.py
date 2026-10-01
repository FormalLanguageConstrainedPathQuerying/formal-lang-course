from networkx import MultiDiGraph

from project.adjacency_matrix_fa import AdjacencyMatrixFA, intersect_automata
from project.automata_utils import graph_to_nfa, regex_to_dfa


def tensor_based_rpq(
    regex: str, graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int]
) -> set[tuple[int, int]]:
    """
    Find vertex pairs connected by a path matching a regular expression.

    Note:
        Paths of length zero are included if the expression accepts the empty word.

    Args:
        regex: Regular expression in the format accepted by regex_to_dfa.
        graph: Directed multigraph with edge symbols in the label attribute.
        start_nodes: Initial vertices; an empty set means all graph vertices.
        final_nodes: Accepting vertices; an empty set independently means all vertices.

    Returns:
        set[tuple[int, int]]: Matching pairs of original graph vertex identifiers.

    Raises:
        ValueError: A specified initial or accepting vertex is absent from the graph.
    """
    graph_fa = AdjacencyMatrixFA(
        graph_to_nfa(graph, set(start_nodes), set(final_nodes))
    )
    regex_fa = AdjacencyMatrixFA(regex_to_dfa(regex))
    product = intersect_automata(graph_fa, regex_fa)
    if not product.start_states or not product.final_states:
        return set()

    start_states = list(product.start_states)
    final_states = list(product.final_states)
    reachable = product.transitive_closure()[start_states][:, final_states].tocoo()

    result = set()
    for row, column in zip(reachable.row, reachable.col):
        source, _ = product.states[start_states[row]].value
        target, _ = product.states[final_states[column]].value
        result.add((source, target))

    return result
