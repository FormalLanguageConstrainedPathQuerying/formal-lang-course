from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from pyformlang.finite_automaton import DeterministicFiniteAutomaton
import project.task02 as fa
import project.task01 as graphs
import pytest

import tempfile
import networkx as nx


@pytest.fixture
def simple_regex():
    return "a*b"


@pytest.fixture
def simple_graph():
    graph = nx.MultiDiGraph()
    graph.add_edge(0, 1, label="a")
    graph.add_edge(1, 2, label="b")
    return graph


def test_regex_to_dfa(simple_regex):
    dfa = fa.regex_to_dfa(simple_regex)
    assert isinstance(dfa, DeterministicFiniteAutomaton)


def test_graph_to_nfa(simple_graph):
    starts = [0]
    finals = [2]
    nfa = fa.graph_to_nfa(simple_graph, starts, finals)
    assert isinstance(nfa, NondeterministicFiniteAutomaton)


def test_two_cycle():
    with tempfile.NamedTemporaryFile() as tmp:
        path = tmp.name

    tcg = graphs.two_cycle_graph_to_dot(path, 4, 4)
    nfa = fa.graph_to_nfa(tcg)

    assert nfa.get_number_transitions() == 10
    assert nfa.start_states == {0, 1, 2, 3, 4, 5, 6, 7, 8}
    assert nfa.final_states == {0, 1, 2, 3, 4, 5, 6, 7, 8}
