import filecmp
import os

import cfpq_data
import networkx
from networkx.algorithms.isomorphism import (
    categorical_multiedge_match,
    categorical_node_match,
)

from project.graph_utils import *

test_dir_path = os.path.dirname(os.path.abspath(__file__))


def test_create_labeled_two_cycles_graph():
    expected_graph = cfpq_data.labeled_two_cycles_graph(
        n=42,
        m=29,
        labels=("c", "d"),
    )
    actual_graph = create_two_cycle_labeled_graph(
        size_of_first_cycle=42, size_of_second_cycle=29, edge_labels=("c", "d")
    )
    assert networkx.is_isomorphic(
        G1=actual_graph,
        G2=expected_graph,
        node_match=categorical_node_match("label", None),
        edge_match=categorical_multiedge_match("label", None),
    )


def test_create_labeled_two_cycles_graph_and_save():
    create_and_save_two_cycle_labeled_graph(
        size_of_first_cycle=42,
        size_of_second_cycle=29,
        edge_labels=("x", "y"),
        file=os.sep.join([test_dir_path, "actual_graph.dot"]),
    )
    assert filecmp.cmp(
        os.sep.join([test_dir_path, "actual_graph.dot"]),
        os.sep.join([test_dir_path, "expected_graph.dot"]),
    )
    os.remove(os.sep.join([test_dir_path, "actual_graph.dot"]))
