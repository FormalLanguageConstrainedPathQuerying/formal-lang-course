import pytest

# on import will print something from __init__ file
import project.graph_utils as utils


def setup_module(module):
    ...


def teardown_module(module):
    ...


def test_get_graph():
    graph = utils.get_graph("generations")
    assert graph.number_of_edges() == 273
    assert graph.number_of_nodes() == 129

    graph = utils.get_graph("bzip")
    assert graph.number_of_edges() == 556
    assert graph.number_of_nodes() == 632


def test_get_labeled_two_cycle_graph():
    graph = utils.get_labeled_two_cycle_graph(5, 5)
    assert graph.number_of_edges() == 12
    assert graph.number_of_nodes() == 11
    assert list(graph.edges(data="label"))[0][2] == "a"
    assert list(graph.edges(data="label"))[10][2] == "b"

    graph = utils.get_labeled_two_cycle_graph(10, 4, ("labe1 1", "label 2"))
    assert graph.number_of_edges() == 16
    assert graph.number_of_nodes() == 15
    assert list(graph.edges(data="label"))[0][2] == "labe1 1"
    assert list(graph.edges(data="label"))[12][2] == "label 2"
