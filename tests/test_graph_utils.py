import os
import networkx as nx
from project import graph_utils


def test_get_graph_info():
    graph = graph_utils.get_graph_info("biomedical")

    assert graph[0] == 341
    assert graph[1] == 459
    assert graph[2] == {
        "subClassOf",
        "label",
        "type",
        "comment",
        "title",
        "language",
        "publisher",
        "description",
        "creator",
        "versionInfo",
    }


def test_save_two_cycles_graph_in_dot():
    graph_utils.save_two_cycles_graph_in_dot(
        10, 20, ("first", "second"), "resources/actual.dot"
    )
    graph_actual: nx.MultiDiGraph = nx.nx_pydot.read_dot("resources/actual.dot")
    os.remove("resources/actual.dot")
    graph_expected: nx.MultiDiGraph = nx.nx_pydot.read_dot("resources/expected.dot")

    assert graph_actual.nodes == graph_expected.nodes
    assert graph_actual.edges == graph_expected.edges
