from project import rpq_bfs_reg_str
import networkx as nx
from test_graphs import all_test_graphs, banana_ananas, empty_graph, labels_as_nodes


def test_rpq_bfs_banana_ananas():
    graph = nx.MultiDiGraph()
    graph.add_edge(0, 1, label="b")
    graph.add_edge(1, 2, label="a")
    graph.add_edge(2, 1, label="n")
    graph.add_edge(2, 3, label="s")
    res = rpq_bfs_reg_str(graph, banana_ananas().reg, {0})
    assert res == {2, 3}


def test_rpq_bfs_separated_banana_ananas():
    graph = nx.MultiDiGraph()
    graph.add_edge(0, 1, label="b")
    graph.add_edge(1, 2, label="a")
    graph.add_edge(2, 1, label="n")
    graph.add_edge(2, 3, label="s")
    res = rpq_bfs_reg_str(graph, banana_ananas().reg, {0}, separated=True)
    assert res == {(0, 2), (0, 3)}
    res = rpq_bfs_reg_str(graph, banana_ananas().reg, {0, 1, 3}, separated=True)
    assert res == {(0, 2), (0, 3), (1, 3)}
    res = rpq_bfs_reg_str(graph, banana_ananas().reg, {1, 2, 3}, separated=True)
    assert res == {(1, 3), (2, 3)}
    res = rpq_bfs_reg_str(graph, banana_ananas().reg, {0, 1, 2, 3}, separated=True)
    assert res == {(0, 2), (0, 3), (1, 3), (2, 3)}


def test_rpq_bfs_empty_some():
    empty = empty_graph()
    for some in all_test_graphs:
        for a, b in ((some, empty), (empty, some)):
            assert (
                len(rpq_bfs_reg_str(a.graph, b.reg, a.start_states)) == 0
            ), f"graph_find_path({a.name}, {b.name}) is not empty set"


def test_rpq_by_reg_str_from_start_labels_as_nodes():
    graph = labels_as_nodes()
    res = rpq_bfs_reg_str(graph.graph, graph.reg, graph.start_states)
    assert res == {"b"}
