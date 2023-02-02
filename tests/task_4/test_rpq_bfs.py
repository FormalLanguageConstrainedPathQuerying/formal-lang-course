import networkx as nx
import pytest
from pyformlang.regular_expression import Regex

from project.automata_tools import create_nfa_from_graph, regex_to_minimal_dfa
from project.boolean_matrices import BooleanMatrices
from project.rpq_bfs import rpq_bfs
from tests.utils import read_data_from_json, dot_to_graph


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
    read_data_from_json(
        "test_rpq_bfs",
        lambda data: (
            dot_to_graph(data["graph"]),
            Regex(data["regex"]),
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
    if not mode:
        bfs = rpq_bfs(graph, regex, starts, finals)
        assert bfs == expected
        if mode:
            assert dict_to_pairs(bfs) == bfs_res
        else:
            assert list(bfs) == bfs_res
    else:
        pass
