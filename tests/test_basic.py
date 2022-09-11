import os

import pydot
import pytest
from project import graph  # on import will print something from __init__ filez


def setup_module(module):
    print("basic setup module")


def teardown_module(module):
    print("basic teardown module")


def test_get_graph_info():
    (n, e, lab) = graph.get_graph_info("bzip")
    assert n == 632 and e == 556 and lab == {"A", "D"}


def test_two_cycles_graph_to_file():
    filename = "test.dot"

    graph.two_cycles_graph_to_file(10, 14, ("H", "M"), filename)

    g = pydot.graph_from_dot_file(filename)[0]

    os.remove(filename)

    assert len(list(g.get_nodes())) == 26
