import networkx
from cfpq_data import labeled_two_cycles_graph
import networkx.algorithms.isomorphism as iso
from project.graph_utility.graph_utility import *


def test_create_graph_of_two_cycles():
    n = 5
    m = 3
    labels = ("a", "b")
    actual_graph = create_graph_of_two_cycles(
        first_cycle_nodes=n, second_cycle_nodes=m, labels=labels
    )
    expected_graph = labeled_two_cycles_graph(n=n, m=m, labels=labels)

    assert expected_graph.nodes == actual_graph.nodes
    assert list(expected_graph.edges.data(data="label")) == list(
        actual_graph.edges.data(data="label")
    )
