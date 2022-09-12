import networkx

from project.graph_utils import *

from networkx.algorithms.isomorphism import (
    categorical_multiedge_match,
    categorical_node_match,
)


def test_create_labeled_two_cycles_graph():
    expected_graph = cfpq_data.labeled_two_cycles_graph(
        n=4,
        m=4,
        labels=("A", "B"),
    )
    actual_graph = build_two_cycle_labeled_graph(
        first_cycle_size=4, second_cycle_size=4, edge_labels=("A", "B")
    )
    assert networkx.isomorphism.is_isomorphic(
        G1=actual_graph,
        G2=expected_graph,
        node_match=categorical_node_match("label", None),
        edge_match=categorical_multiedge_match("label", None),
    )
