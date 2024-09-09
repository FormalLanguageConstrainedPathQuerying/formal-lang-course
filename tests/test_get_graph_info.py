import pytest
import networkx as nx
from project.task1 import GraphInfo, load_graph_info


def test_get_graph_info():
    exp_num_nodes = 632
    exp_num_edg = 556
    exp_labels = ["d", "a"]

    bzip_actual = load_graph_info("bzip")
    assert GraphInfo(exp_num_nodes, exp_num_edg, exp_labels) == bzip_actual
