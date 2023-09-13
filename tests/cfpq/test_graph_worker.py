from os import path

from networkx import Graph, MultiDiGraph

from project.cfpq.graph_worker import GraphWorker


def test_empty_graph():
    graph = Graph()
    expected = {"num_of_nodes": 0, "num_of_edges": 0, "set_of_labels": set()}

    gw = GraphWorker()
    gw.update_graph(graph)

    assert expected == gw.get_graph_info()


def test_load_graph_by_name():
    gw = GraphWorker()
    gw.load_graph_by_name("bzip")
    actual = gw.get_graph_info()

    assert 632 == actual["num_of_nodes"]
    assert 556 == actual["num_of_edges"]
    assert {"a", "d"} == actual["set_of_labels"]


def test_save_as_dot_file():
    graph = MultiDiGraph()
    for i in [5, 10, 15]:
        graph.add_node(i)
    graph.add_edge(5, 15, label="a")
    graph.add_edge(15, 10, label="b")
    graph.add_edge(10, 5, label="c")

    curr_path = path.dirname(path.realpath(__file__))
    expected_path = path.join(curr_path, "expected_graph_gw.dot")
    actual_path = path.join(curr_path, "actual_graph_gw.dot")

    gw = GraphWorker()
    gw.update_graph(graph)

    is_created = gw.save_as_dot_file(actual_path)

    assert is_created

    with open(expected_path, "r") as expected_file:
        with open(actual_path, "r") as actual_file:
            assert expected_file.read() == actual_file.read()
