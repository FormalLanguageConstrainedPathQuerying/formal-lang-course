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
    graph_utils.save_two_cycles_graph_in_dot(10, 20, ("first", "second"), "temp.dot")
    graph: nx.MultiDiGraph = nx.nx_pydot.read_dot("temp.dot")
    graph.remove_node("\\n")
    os.remove("temp.dot")

    assert graph.number_of_nodes() == 31
    assert graph.number_of_edges() == 32
    assert graph.edges["1", "2", "0"]["label"] == "first"
    assert graph.edges["21", "22", "0"]["label"] == "second"
