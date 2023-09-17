import networkx
import pytest

from project.graphs.io import *


def test_load_graph():
    with pytest.raises(Exception):
        load_graph("not_exists")


def test_load_generations():
    graph_info = load_graph_info("generations")

    assert graph_info[0] == 273
    assert graph_info[1] == 129
    assert graph_info[2] == {
        "hasSibling",
        "someValuesFrom",
        "versionInfo",
        "sameAs",
        "oneOf",
        "range",
        "first",
        "type",
        "hasValue",
        "equivalentClass",
        "intersectionOf",
        "inverseOf",
        "hasParent",
        "onProperty",
        "rest",
        "hasChild",
        "hasSex",
    }


def test_load_bzip():
    graph_info = load_graph_info("bzip")

    assert graph_info[0] == 556
    assert graph_info[1] == 632
    assert graph_info[2] == {"d", "a"}


def test_labeled_two_cycles_graph_as_dot():
    actual_path = "./resources/actual1.dot"
    expected_path = "./resources/expected1.dot"
    save_labeled_two_cycles_graph_as_dot(3, 4, ("abc", "def"), actual_path)

    expected = Path(expected_path)
    actual = Path(actual_path)

    with open(expected, "r") as expected_file:
        with open(actual, "r") as actual_file:
            assert expected_file.read() == actual_file.read()


def test_save_graph_as_dot():
    graph = networkx.MultiDiGraph()
    graph.add_edge(3, 4, label="abc")
    graph.add_edge(1, 7, label="xyz")
    graph.add_edge(6, 9, label="lol")

    actual_path = "./resources/actual2.dot"
    expected_path = "./resources/expected2.dot"
    save_graph_as_dot(graph, actual_path)
    expected = Path(expected_path)
    actual = Path(actual_path)

    with open(expected, "r") as expected_file:
        with open(actual, "r") as actual_file:
            assert expected_file.read() == actual_file.read()
