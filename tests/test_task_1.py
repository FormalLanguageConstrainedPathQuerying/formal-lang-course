from project import get_graph_info_by_name, create_labeled_two_cycles_graph

import networkx as nx
from typing import Set

import pytest


@pytest.fixture()
def start():
    print("Start test")


def test_get_graph_info_by_name_bzip():
    assert get_graph_info_by_name("bzip") == (632, 556, {"d", "a"})


def test_get_graph_info_by_name_generations():
    labels: Set = {
        "inverseOf",
        "sameAs",
        "hasParent",
        "intersectionOf",
        "hasSex",
        "range",
        "onProperty",
        "someValuesFrom",
        "rest",
        "first",
        "oneOf",
        "hasValue",
        "hasSibling",
        "hasChild",
        "versionInfo",
        "type",
        "equivalentClass",
    }

    assert get_graph_info_by_name("generations") == (129, 273, labels)


def test_create_labeled_two_cycles_graph(path: str = "graph.dot"):
    create_labeled_two_cycles_graph(n=5, m=4, labels=("a", "b"), path=path)

    graph = nx.Graph(nx.nx_pydot.read_dot(path))

    assert list(graph.nodes) == ["1", "2", "3", "4", "5", "0", "6", "7", "8", "9"]
    assert list(graph.edges) == [
        ("1", "2"),
        ("1", "0"),
        ("2", "3"),
        ("3", "4"),
        ("4", "5"),
        ("5", "0"),
        ("0", "6"),
        ("0", "9"),
        ("6", "7"),
        ("7", "8"),
        ("8", "9"),
    ]
