import pytest
import networkx as nx

# on import will print something from __init__ file
from project import graph_utils as gu


def test_saving_to_file():
    path = "tmp.dot"
    num1, num2 = 3, 4
    label1, label2 = "one", "two"
    two_cycle = gu.generate_two_cycles_graph(num1, num2, (label1, label2), path)
    cycle_from_file = nx.nx_pydot.read_dot(path)
    assert gu.number_of_edges(cycle_from_file) == gu.number_of_edges(two_cycle)
    assert gu.number_of_nodes(cycle_from_file) == gu.number_of_nodes(two_cycle)
    assert gu.unique_labels(cycle_from_file) == gu.unique_labels(two_cycle)


def test_graph_generation():
    num1, num2 = 3, 4
    label1, label2 = "one", "two"
    two_cycle = gu.generate_two_cycles_graph(num1, num2, (label1, label2))
    assert gu.number_of_edges(two_cycle) == (num1 + num2 + 2)
    assert gu.number_of_nodes(two_cycle) == (num1 + num2 + 1)
    assert gu.unique_labels(two_cycle) == {label1, label2}


def test_graph_loading():
    avrora_graph = gu.load_graph_by_name("avrora")
    assert isinstance(avrora_graph, nx.MultiDiGraph)
