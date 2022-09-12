import networkx
import filecmp
import os

from project.graph_utils import *

from networkx.algorithms.isomorphism import (
    categorical_multiedge_match,
    categorical_node_match,
)

test_dir_path = os.path.dirname(os.path.abspath(__file__))


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


def test_create_labeled_two_cycles_graph_and_save():
    build_and_save_two_cycle_labeled_graph(
        first_cycle_size=3,
        second_cycle_size=3,
        edge_labels=("A", "B"),
        file=os.sep.join([test_dir_path, "actual_graph.dot"]),
    )
    assert filecmp.cmp(
        os.sep.join([test_dir_path, "actual_graph.dot"]),
        os.sep.join([test_dir_path, "sample_graph.dot"]),
    )
    os.remove(os.sep.join([test_dir_path, "actual_graph.dot"]))
