import filecmp
import os
import unittest

from project.g_util import *


class GUtilTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_wc_from_dataset(self):
        graph = load_graph("wc")
        graph_info = get_graph_information(graph)
        assert graph_info == GraphInformation(nodes=332, edges=269, edges_labels={"A", "D"})

    def test_build_2_cycles(self):
        graph = build_two_cycle_labeled_graph(42, 29, edge_labels=("A", "B"))
        save_graph(graph, "G")
        assert filecmp.cmp("G", "./tests/expected_2_cycles_graph")
        os.remove("G")
