import unittest

from project import g_util, regex_util
from project.matrix_util import *

from pyformlang.finite_automaton import (NondeterministicFiniteAutomaton, State)

from project.rpq import rpq_to_graph_tc, rpq_to_graph_bfs_all_reachable, rpq_to_graph_bfs


class MatrixUtilTest(unittest.TestCase):
    def setUp(self):
        pass

    def test_transitive_closure(self):
        nfa = NondeterministicFiniteAutomaton()
        nfa.add_transitions([(0, "A", 1), (1, "B", 2), (1, "C", 1), (2, "D", 3), (3, "E", 0)])
        am = AdjacencyMatrix(nfa)
        tc = am.get_transitive_closure()
        assert tc.sum() == tc.size

    def test_intersection_1(self):
        fa1 = NondeterministicFiniteAutomaton()
        fa1.add_transitions([(0, "A", 1), (0, "B", 0), (1, "C", 1), (1, "D", 2), (2, "E", 0)])
        fa1.add_start_state(State(0))
        fa1.add_final_state(State(0))
        fa1.add_final_state(State(1))
        fa1.add_final_state(State(2))
        am1 = AdjacencyMatrix(fa1)

        fa2 = NondeterministicFiniteAutomaton()
        fa2.add_transitions([(0, "A", 1), (1, "Z", 2)])
        fa2.add_start_state(State(0))
        fa2.add_final_state(State(1))
        am2 = AdjacencyMatrix(fa2)

        expected = NondeterministicFiniteAutomaton()
        expected.add_transitions([(0, "A", 1)])
        expected.add_start_state(State(0))
        expected.add_final_state(State(1))

        intersected = intersect_adjacency_matrices(am1, am2)
        actual = adjacency_matrix_to_nfa(intersected)
        assert expected.is_equivalent_to(actual)

    def test_intersection_2(self):
        fa1 = regex_util.regex_to_min_dfa("AB")
        am1 = AdjacencyMatrix(fa1)
        fa2 = regex_util.regex_to_min_dfa("BC")
        am2 = AdjacencyMatrix(fa2)

        expected = NondeterministicFiniteAutomaton()
        expected.add_start_state(State(3))
        expected.add_final_state(State(0))

        intersected = intersect_adjacency_matrices(am1, am2)
        actual = adjacency_matrix_to_nfa(intersected)
        assert expected.is_equivalent_to(actual)

    def test_rpq_tc(self):
        regex = "AAAAAA | B"
        start_nodes = {0}
        final_nodes = {1, 2, 3, 4, 5}
        graph = g_util.build_two_cycle_labeled_graph(4, 3, ("A", "B"))

        actual = rpq_to_graph_tc(graph, regex, start_nodes, final_nodes)
        expected = {(0, 5)}
        assert expected == actual

    def test_rpq_tc_2(self):
        regex = "(A | B)*"
        graph = g_util.build_two_cycle_labeled_graph(1, 2, edge_labels=("A", "B"))

        start_nodes = {0, 2}
        final_nodes = {2, 1}
        actual = rpq_to_graph_tc(graph, regex, start_nodes, final_nodes)
        expected = {(0, 1), (0, 2), (2, 1), (2, 2)}
        assert expected == actual

        start_nodes = {1}
        final_nodes = {0}
        actual = rpq_to_graph_tc(graph, regex, start_nodes, final_nodes)
        expected = {(1, 0)}
        assert expected == actual

    # seEfficiencyWarning: Changing the sparsity structure of a csr_matrix is expensive. lil_matrix is more efficient.
    def test_rpq_bfs(self):
        regex = "AAAAAA | B"
        start_nodes = {0}
        final_nodes = {1, 2, 3, 4, 5}
        graph = g_util.build_two_cycle_labeled_graph(4, 3, ("A", "B"))

        actual = rpq_to_graph_bfs_all_reachable(graph, regex, start_nodes, final_nodes)
        expected = {0: {5}}
        assert expected == actual


    def test_rpq_bfs_2(self):
        regex = "(A | B)*"
        graph = g_util.build_two_cycle_labeled_graph(1, 2, edge_labels=("A", "B"))

        start_nodes = {0, 2}
        final_nodes = {2, 1}
        actual = rpq_to_graph_bfs_all_reachable(graph, regex, start_nodes, final_nodes)
        expected = {0: {1, 2}, 2: {1, 2}}
        assert expected == actual

        start_nodes = {1}
        final_nodes = {0}
        actual = rpq_to_graph_bfs_all_reachable(graph, regex, start_nodes, final_nodes)
        expected = {1: {0}}
        assert expected == actual


    # seEfficiencyWarning: Changing the sparsity structure of a csr_matrix is expensive. lil_matrix is more efficient.
    def test_rpq_bfs(self):
        regex = "AAAAAA | B"
        start_nodes = {0}
        final_nodes = {1, 2, 3, 4, 5}
        graph = g_util.build_two_cycle_labeled_graph(4, 3, ("A", "B"))

        actual = rpq_to_graph_bfs(graph, regex, start_nodes, final_nodes)
        expected = {5}
        assert expected == actual

    def test_rpq_bfs_2(self):
        regex = "(A | B)*"
        graph = g_util.build_two_cycle_labeled_graph(1, 2, edge_labels=("A", "B"))

        start_nodes = {0, 2}
        final_nodes = {2, 1}
        actual = rpq_to_graph_bfs(graph, regex, start_nodes, final_nodes)
        expected = {1, 2}
        assert expected == actual

        start_nodes = {1}
        final_nodes = {0}
        actual = rpq_to_graph_bfs(graph, regex, start_nodes, final_nodes)
        expected = {0}
        assert expected == actual
