from typing import Union, Set, Tuple

import networkx as nx
from pyformlang.cfg import CFG, Variable

from project.hellings import hellings
from project.matrix import matrix


def cfpq_using_matrix(
    graph: nx.Graph,
    query: Union[CFG, str],
    starts: Set[int] = None,
    finals: Set[int] = None,
    start_nonterminal: Union[str, Variable] = "S",
):
    if start_nonterminal is None:
        start_nonterminal = "S"
    if isinstance(start_nonterminal, str):
        start_nonterminal = Variable(start_nonterminal)
    if isinstance(query, str):
        query = CFG.from_text(query, start_nonterminal)
    if starts is None:
        starts = graph.nodes
    if finals is None:
        finals = graph.nodes

    data = matrix(graph, query)

    return {
        (i, v.value, j)
        for (i, v, j) in data
        if i in starts and j in finals and v == start_nonterminal
    }


def cfpq_using_hellings(
    graph: nx.Graph,
    query: Union[CFG, str],
    starts: Set[int] = None,
    finals: Set[int] = None,
    start_nonterminal: Union[str, Variable] = "S",
) -> Set[Tuple[int, int]]:
    if start_nonterminal is None:
        start_nonterminal = "S"
    if isinstance(start_nonterminal, str):
        start_nonterminal = Variable(start_nonterminal)
    if isinstance(query, str):
        query = CFG.from_text(query, start_nonterminal)
    if starts is None:
        starts = graph.nodes
    if finals is None:
        finals = graph.nodes

    data = hellings(graph, query)

    return {
        (v1, v2)
        for (v1, N, v2) in data
        if (v1 in starts and v2 in finals and N == start_nonterminal)
    }
