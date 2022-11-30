import networkx as nx
import pytest
from pyformlang.regular_expression import Regex

from project.boolean_decompositonNFA import BooleanDecompositionNFA
from project.regex_utils import create_nfa_from_graph, regex_to_dfa
from project.rpq_bfs import rpq_bfs, bfs_sync
from tests.utils import get_data, dot_to_graph


def list_of_pairs_to_set(list) -> set:
    acc = set()
    for pair in list:
        acc.add((pair[0], pair[1]))
    return acc


def dict_to_pairs(dict: dict):
    acc = []
    for key in dict.keys():
        acc.append([key, list(dict.get(key))])
    return acc


@pytest.mark.parametrize(
    "graph, regex, starts, finals, expected, mode, bfs_res",
    get_data(
        "test_rpq_bfs",
        lambda data: (
            dot_to_graph(data["graph"]),
            data["regex"],
            set(data["starts"]),
            set(data["finals"]),
            set(data["expected"])
            if not data["for_each"]
            else list_of_pairs_to_set(data["expected"]),
            data["for_each"],
            data["bfs_res"],
        ),
    ),
)
def test_rpq_bfs(
    graph: nx.MultiDiGraph, regex, starts, finals, expected, mode, bfs_res
):
    bfs = bfs_sync(
        graph=BooleanDecompositionNFA(
            create_nfa_from_graph(graph=graph, start_states=starts, final_states=finals)
        ),
        regex=BooleanDecompositionNFA(regex_to_dfa(Regex(regex))),
        is_for_each=mode,
        final_states=finals,
        start_states=starts,
    )
    assert (
        rpq_bfs(
            graph=graph,
            regex=Regex(regex),
            start_states=starts,
            final_states=finals,
            is_for_each=mode,
        )
        == expected
    )
    if mode:
        assert dict_to_pairs(bfs) == bfs_res
    else:
        assert list(bfs) == bfs_res
