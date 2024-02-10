import networkx
import pytest
import project  # on import will print something from __init__ file
from project.graphutils import graph_signature, save_twocycled_graph


def setup_module(module):
    print("intro tests")


def teardown_module(module):
    pass


def test_graph_stats():
    s = graph_signature("ls")
    assert s == (1687, 1453, ["d", "a"])


def test_2cycled_graph():
    save_twocycled_graph(10, 8, ("a", "b"))
    g = networkx.drawing.nx_pydot.read_dot("twocycled_10_8.dot")
    assert g.number_of_nodes() == 19
