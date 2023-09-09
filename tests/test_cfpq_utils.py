import pytest
from networkx import Graph

import project  # on import will print something from __init__ file
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
