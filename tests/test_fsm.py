import pytest
import pyformlang.regular_expression as re
import pyformlang.finite_automaton as fa
import networkx as nx
import cfpq_data as cd

from project.fsm import *


def def_empty_regex_to_dfa():
    dfa = regex_to_dfa(re.Regex(""))
    assert dfa.is_empty()


def test_regex_to_dfa():
    dfa = regex_to_dfa(re.Regex("av|cv"))
    assert dfa.is_deterministic()
    assert dfa.accepts([fa.Symbol("av")])
    assert dfa.accepts([fa.Symbol("cv")])
    assert not dfa.accepts([fa.Symbol("12")])


def test_empty_graph_to_nfa():
    nfa = graph_to_nfa(nx.MultiDiGraph())
    assert nfa.is_empty()


def test_graph_to_nfa():
    graph = cd.labeled_two_cycles_graph(5, 5, labels=("A", "B"))
    actual_nfa = graph_to_nfa(graph, {0}, {3, 2})

    expected = fa.NondeterministicFiniteAutomaton()
    expected.add_start_state(fa.State(0))
    expected.add_final_state(fa.State(3))
    expected.add_final_state(fa.State(2))
    for fr, to, label in graph.edges(data="label"):
        expected.add_transition(fa.State(fr), fa.Symbol(label), fa.State(to))

    assert actual_nfa.is_equivalent_to(expected)
