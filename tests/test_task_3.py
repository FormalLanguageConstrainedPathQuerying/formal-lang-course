import pytest
import networkx as nx
from pyformlang.regular_expression import Regex

from project.automata_builder import get_nfa_from_graph
from project.task_3 import *


def nfa_a():
    graphA = nx.MultiDiGraph()
    graphA.add_nodes_from([0, 1])

    graphA.add_edge(0, 0, label="0")
    graphA.add_edge(0, 1, label="1")

    graphA.add_edge(1, 1, label="0")
    graphA.add_edge(1, 1, label="1")

    return get_nfa_from_graph(graphA, start=[0], final=[1])


def nfa_b():
    graphB = nx.MultiDiGraph()
    graphB.add_nodes_from([0, 1, 2])

    graphB.add_edge(0, 1, label="0")
    graphB.add_edge(0, 0, label="1")

    graphB.add_edge(1, 1, label="0")
    graphB.add_edge(1, 2, label="1")

    graphB.add_edge(2, 2, label="0")
    graphB.add_edge(2, 2, label="1")

    return get_nfa_from_graph(graphB, start=[0], final=[2])


def intersection_for_test():
    nfaA = nfa_a()

    nfaB = nfa_b()

    return intersect_finite_automata(nfaA, nfaB)


def test_intersection_1():
    nfa = intersection_for_test()
    nfaA = nfa_a()
    nfaB = nfa_b()

    word = ["0", "0", "1", "0"]

    assert nfa.accepts(word) == (nfaA.accepts(word) and nfaB.accepts(word))


def test_intersection_2():
    nfa = intersection_for_test()
    nfaA = nfa_a()
    nfaB = nfa_b()

    word = ["0", "0", "0", "0"]

    assert nfa.accepts(word) == (nfaA.accepts(word) and nfaB.accepts(word))


def test_intersection_3():
    nfa = intersection_for_test()
    nfaA = nfa_a()
    nfaB = nfa_b()

    word = ["1", "1", "1", "1"]

    assert nfa.accepts(word) == (nfaA.accepts(word) and nfaB.accepts(word))


def test_intersection_4():
    nfa = intersection_for_test()
    nfaA = nfa_a()
    nfaB = nfa_b()

    word = ["1", "1", "1", "0", "0", "0", "0"]

    assert nfa.accepts(word) == (nfaA.accepts(word) and nfaB.accepts(word))


def test_regex_path_1():
    regex = Regex("a")

    graph = nx.MultiDiGraph()
    graph.add_nodes_from([0, 1])
    graph.add_edge(0, 1, label="a")
    starts = [0]
    finals = [1]

    assert regex_path_in_automaton(regex, graph, starts, finals) == {(0, 1)}


def test_regex_path_2():
    regex = Regex("a|b")

    graph = nx.MultiDiGraph()
    graph.add_nodes_from([0, 1, 2])
    graph.add_edge(0, 1, label="a")
    graph.add_edge(0, 2, label="b")
    starts = [0]
    finals = [1, 2]

    assert regex_path_in_automaton(regex, graph, starts, finals) == {(0, 1), (0, 2)}


def test_regex_path_3():
    regex = Regex("a*")

    graph = nx.MultiDiGraph()
    graph.add_nodes_from([0, 1, 2])
    graph.add_edge(0, 1, label="a")
    graph.add_edge(1, 2, label="a")
    starts = [0, 1]
    finals = [1, 2]

    assert regex_path_in_automaton(regex, graph, starts, finals) == {
        (0, 1),
        (0, 2),
        (1, 1),
        (1, 2),
    }
