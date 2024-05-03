import unittest
from project import *
import pydot


class Test_get_nvertex_nedges_numerate_marks(unittest.TestCase):
    def test_get_nvertex_nedges_numerate_marks(self):
        a1, a2, ls = get_nvertex_nedges_numerate_marks("bzip")
        self.assertEqual(a1, 632, "Should be 632")
        self.assertEqual(a2, 556, "Should be 556")
        self.assertTrue(len(ls) != 0)


class Test_create_labeled_two_cycles_graph(unittest.TestCase):
    def test_create_labeled_two_cycles_graph(self):
        self.assertEqual(
            create_labeled_two_cycles_graph("tmp.dot", 2, 2, ("a", "b")),
            True,
            "Should be 1",
        )
        graph_ = pydot.graph_from_dot_file("tmp.dot")[0]
        gr = networkx.nx_pydot.from_pydot(graph_)
        self.assertEqual(gr.number_of_nodes(), 5)
