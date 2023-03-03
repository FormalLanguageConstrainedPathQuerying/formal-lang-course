import pytest
import project.graphs as graphs
import networkx as nx
import os


def test_info_skos():
    info_skos = graphs.get_graph_info("skos")
    skos_nodes = 144
    skos_edges = 252
    skos_labels = 21
    assert skos_nodes == info_skos.number_of_nodes
    assert skos_edges == info_skos.number_of_edges
    assert skos_labels == len(info_skos.labels)


def test_info_travel():
    info_travel = graphs.get_graph_info("travel")
    travel_nodes = 131
    travel_edges = 277
    travel_labels = 22
    assert travel_nodes == info_travel.number_of_nodes
    assert travel_edges == info_travel.number_of_edges
    assert travel_labels == len(info_travel.labels)


def test_two_cycles_eq():
    file_name = "test_two_cycles_eq_here"
    n = 3
    m = 4
    labels = ("uno", "duo")

    graphs.save_two_cycles(n, m, labels, file_name)
    gr = nx.nx_pydot.read_dot(file_name)

    if os.path.exists(file_name):
        os.remove(file_name)
    assert isinstance(gr, nx.MultiDiGraph)
    if isinstance(gr, nx.MultiDiGraph):
        assert n + m + 1 == gr.number_of_nodes()
        assert n + m + 2 == gr.number_of_edges()
        unique_labels = set(
            (e[2] if (3 <= len(e)) else None) for e in gr.edges(data="label")
        )
        unique_labels.discard(None)
        assert {"uno", "duo"} == unique_labels
