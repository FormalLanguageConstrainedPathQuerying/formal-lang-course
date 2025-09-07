from project.graph_info import *
import networkx as nx
import os
import pytest
import pydot

def setup_module(module):
    print("basic setup module")


def teardown_module(module):
    print("basic teardown module")


def test_get_graph_info_wc():
    info = get_graph_info("wc")
    assert info.node_num == 332
    assert info.edge_num == 269
    assert info.labels == ["d", "a"]


def test_get_graph_info_notexist():
    with pytest.raises(FileNotFoundError):
        get_graph_info("Pridnestrovie")


def test_save_graph():
    n, m, labels = 3, 9, ["h", "m"]
    filename = "tests/out_test_save_graph.dot"

    save_two_cycle_graph(n, m, labels, filename)
    graph = nx.drawing.nx_pydot.read_dot(filename)

    assert graph.number_of_nodes() == n + m + 1
    assert set(cfpq_data.get_sorted_labels(graph)) == set(labels)
