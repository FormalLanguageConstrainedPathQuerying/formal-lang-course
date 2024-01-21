import pytest
from project.automata_builder import *
import networkx as nx

from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton


def test_equivalence_1():
    regex = Regex("(a|b|c) (d|e|f)")
    dfa = get_dfa_from_regex(regex)

    assert regex.accepts(["a", "d"]) == dfa.accepts(["a", "d"])


def test_equivalence_2():
    regex = Regex("abc|d")
    dfa = get_dfa_from_regex(regex)

    assert regex.accepts(["d"]) == dfa.accepts(["d"])


def test_equivalence_3():
    regex = Regex("abc|d")
    dfa = get_dfa_from_regex(regex)

    assert regex.accepts(["a", "b", "c"]) == dfa.accepts(["a", "b", "c"])


def nfa_for_tests():
    graph = nx.MultiDiGraph()
    graph.add_nodes_from([0, 1, 2])

    graph.add_edges_from([(0, 1, dict(label="a")), (0, 0, dict(label="b"))])
    graph.add_edges_from([(1, 2, dict(label="a")), (1, 1, dict(label="b"))])
    graph.add_edges_from([(2, 0, dict(label="a")), (2, 2, dict(label="b"))])

    return get_nfa_from_graph(graph, start=[0], final=[0])


def test_graph_the_amount_of_a_mod_3_is_0_correct_1():
    nfa = nfa_for_tests()

    assert nfa.accepts("aaa") == True


def test_graph_the_amount_of_a_mod_3_is_0_correct_2():
    nfa = nfa_for_tests()

    assert nfa.accepts("abbbaabababbaababa") == True


def test_graph_the_amount_of_a_mod_3_is_0_incorrect_1():
    nfa = nfa_for_tests()

    assert nfa.accepts("aa") == False


def test_graph_the_amount_of_a_mod_3_is_0_incorrect_2():
    nfa = nfa_for_tests()

    assert nfa.accepts("abbbaababaabbaababa") == False
