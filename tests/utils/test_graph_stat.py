import os

import pytest
import filecmp
from project.utils.graph_utils import *


def test_graph_data():
    stat = get_graph_data(load_graph("bzip"))
    assert stat.num_of_nodes == 632
    assert stat.num_of_edges == 556
    assert stat.set_of_labels == set({"d", "a"})


def test_draw_graph():
    path = os.path.dirname(os.path.realpath(__file__))
    actual_file = f"{path}/actual_graph.dot"
    expected_file = f"{path}/expected_graph.dot"
    draw_graph(build_two_cycles_graph(2, 3, ("a", "b")), actual_file)
    assert filecmp.cmp(expected_file, actual_file)
