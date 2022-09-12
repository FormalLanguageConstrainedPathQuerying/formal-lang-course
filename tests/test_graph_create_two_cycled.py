import networkx

from project.graph_utils import *


def test_create_labeled_two_cycles_graph():
    expected_graph = cfpq_data.labeled_two_cycles_graph(
        n=4,
        m=4,
        labels=('A', 'B'),
    )
    actual_graph = build_two_cycle_labeled_graph(
        first_cycle_size=4,
        second_cycle_size=4,
        edge_labels=('A', 'B')
    )
    assert networkx.isomorphism.is_isomorphic(actual_graph, expected_graph)