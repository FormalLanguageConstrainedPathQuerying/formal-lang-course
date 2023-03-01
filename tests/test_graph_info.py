import os
import pytest
import networkx as nx
import cfpq_data as cd

from project.graph_utils import *

graphs = [
    cd.graph_from_csv(cd.download("skos")),
    cd.graph_from_csv(cd.download("wc")),
    cd.graph_from_csv(cd.download("generations")),
]


def is_graphs_equal(g, g1):
    return (
        g.edges == g1.edges
        and g.nodes == g1.nodes
        and get_edges_labels(g) == get_edges_labels(g1)
    )


def test_load_graph():
    names = ["skos", "wc", "generations"]
    for i in range(3):
        loaded_graph = load_graph(names[i])
        assert is_graphs_equal(graphs[i], loaded_graph)


def test_save_graph():
    save_graph(graphs[0], "skos")
    assert "skos" in os.listdir(".")
    os.remove("skos")


def test_get_vertices_number():
    for graph in graphs:
        assert get_vertices_number(graph) == graph.number_of_nodes()


def test_get_edges_number():
    for graph in graphs:
        assert get_edges_number(graph) == graph.number_of_edges()


def test_get_edges_labels():
    assert get_edges_labels(graphs[1]) == {"d", "a"}


def test_build_two_cycle_graph():
    n = 8
    m = 10
    labels = ("A", "B")
    my_graph = build_two_cycle_graph(n, m, labels)
    sample_graph = cd.labeled_two_cycles_graph(n, m, labels=labels)
    assert is_graphs_equal(my_graph, sample_graph)


def test_build_and_save_two_cycle_graph():
    n = 8
    m = 10
    labels = ("A", "B")
    filename = "saved_graph"
    my_graph = build_and_save_two_cycle_graph(n, m, labels, filename)
    sample_graph = cd.labeled_two_cycles_graph(n, m, labels=labels)
    assert is_graphs_equal(my_graph, sample_graph)
    assert "saved_graph" in os.listdir(".")
    os.remove("saved_graph")
