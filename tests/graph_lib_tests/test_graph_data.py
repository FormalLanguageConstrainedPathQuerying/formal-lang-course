from project.graph_lib import *


def test_graph_data_get_1():
    G = MultiDiGraph()
    G.add_nodes_from([0, 1, 2, 3])
    G.add_edges_from([
        (0, 1, {"label": "a"}), 
        (0, 2, {"label": "a"}), 
        (3, 3, {"label": "b"})
    ])
    graph_data = get_graph_data(G)

    assert graph_data.node_count == 4
    assert graph_data.edge_count == 3
    assert graph_data.labels == {"a", "b"}


def test_graph_data_get_2():
    G = MultiDiGraph()
    G.add_nodes_from([0])
    G.add_edges_from([(0, 0, {"label": "a"})])
    graph_data = get_graph_data(G)

    assert graph_data.node_count == 1
    assert graph_data.edge_count == 1
    assert graph_data.labels == {"a"}


def test_graph_data_get_3():
    G = MultiDiGraph()
    G.add_nodes_from([0, 1, 2, 3, 4])
    graph_data = get_graph_data(G)

    assert graph_data.node_count == 5
    assert graph_data.edge_count == 0
    assert graph_data.labels == set()


def test_get_graph_data_bzip():
    graph_data = get_graph_data_by_name("bzip")

    assert graph_data.node_count == 632
    assert graph_data.edge_count == 556
    assert graph_data.labels == {"a", "d"}


def test_get_graph_data_skos():
    graph_data = get_graph_data_by_name("skos")

    expected_labels = {
        "comment",
        "contributor",
        "creator",
        "definition",
        "description",
        "disjointWith",
        "domain",
        "example",
        "first",
        "inverseOf",
        "isDefinedBy",
        "label",
        "range",
        "rest",
        "scopeNote",
        "seeAlso",
        "subClassOf",
        "subPropertyOf",
        "title",
        "type",
        "unionOf",
    }

    assert graph_data.node_count == 144
    assert graph_data.edge_count == 252
    assert graph_data.labels == expected_labels
