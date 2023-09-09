from networkx import Graph, MultiDiGraph

from project.cfpq.graph_info import GraphInfo
from project.cfpq.utils import get_graph_info


def setup_module(module):
    print("basic setup module")


def teardown_module(module):
    print("basic teardown module")


def test_get_graph_info_empty_graph():
    graph = Graph()
    graph_info = GraphInfo()

    assert graph_info == get_graph_info(graph)


def test_get_graph_info_nonempty_graph():
    graph = MultiDiGraph()
    graph.add_node(1)
    graph.add_node(2)
    graph.add_node(3)
    graph.add_node(4)
    graph.add_node(5)
    graph.add_edge(1, 3, label="a")
    graph.add_edge(2, 3, label="b")
    graph.add_edge(4, 1, label="a")
    graph.add_edge(1, 4, label="c")

    graph_info = GraphInfo(
        number_of_nodes=5, number_of_edges=4, unique_labels={"a", "b", "c"}
    )

    assert graph_info == get_graph_info(graph)
