import filecmp
import os
import networkx

from networkx import nx_pydot, MultiDiGraph
from project.graph_manager import GraphManager
from project.cfg_manager import CFGManager
from pyformlang.cfg import Variable

path = os.path.dirname(os.path.abspath(__file__)) + "/res"


def test_write_two_cycle_labeled_graph_to_dot():
    path = os.path.dirname(os.path.abspath(__file__)) + "/res"
    actual = path + "/actual.dot"
    expected = path + "/expected.dot"

    GraphManager.create_two_cycle_labeled_graph((2, 3), ("a", "b"), actual)
    filecmp.cmp(actual, expected)
    os.remove(actual)


def test_create_two_cycle_labeled_graph():
    path = os.path.dirname(os.path.abspath(__file__)) + "/res/expected.dot"
    expected = nx_pydot.read_dot(path)

    sizes = (2, 3)
    labels = ("a", "b")
    actual = GraphManager._GraphManager__create_two_cycle_labeled_graph(sizes, labels)

    networkx.is_isomorphic(
        actual,
        expected,
        node_match=expected.nodes,
        edge_match=expected.edges(data=True),
    )


def test_execute_cfpq():
    graph_edges = [
        (0, 1, {"label": "a"}),
        (1, 2, {"label": "a"}),
        (2, 0, {"label": "a"}),
        (2, 3, {"label": "b"}),
        (3, 2, {"label": "b"}),
    ]

    expected_cfg = {(0, 3), (2, 3)}

    expected_hellings = [
        (Variable("A"), 0, 1),
        (Variable("A"), 1, 2),
        (Variable("A"), 2, 0),
        (Variable("B"), 2, 3),
        (Variable("B"), 3, 2),
        (Variable("S"), 1, 3),
        (Variable("C"), 1, 2),
        (Variable("S"), 0, 2),
        (Variable("C"), 0, 3),
        (Variable("S"), 2, 3),
        (Variable("C"), 2, 2),
        (Variable("S"), 1, 2),
        (Variable("C"), 1, 3),
        (Variable("S"), 0, 3),
        (Variable("C"), 0, 2),
        (Variable("S"), 2, 2),
        (Variable("C"), 2, 3),
    ]

    start_nodes = {0, 2}
    final_nodes = {3}

    cfg = CFGManager.read_cfg_from_file(path + "/cfg_3")

    graph = MultiDiGraph()
    graph.add_edges_from(graph_edges)

    actual_cfpq = GraphManager.execute_cfpq(
        cfg, graph, start_nodes=start_nodes, final_nodes=final_nodes
    )
    actual_hellings = GraphManager._GraphManager__run_hellings(cfg, graph)

    assert actual_cfpq == expected_cfg

    for triple in actual_hellings:
        if triple not in expected_hellings:
            assert False

    for triple in expected_hellings:
        if triple not in expected_hellings:
            assert False
