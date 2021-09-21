from project.utils.automata_utils import transform_graph_to_nfa
from project.utils.automata_utils import AutomataException
from project.utils.graph_utils import generate_two_cycles_graph
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State, Symbol

import pytest
import networkx as nx


@pytest.fixture
def default_graph():
    return generate_two_cycles_graph("2", "2", "x", "y")


@pytest.fixture
def default_nfa():
    nfa = NondeterministicFiniteAutomaton()
    nfa.add_transitions(
        [(1, "x", 2), (2, "x", 0), (0, "x", 1), (0, "y", 3), (3, "y", 4), (4, "y", 0)]
    )

    return nfa


@pytest.fixture
def default_start_states():
    return {1, 3}


@pytest.fixture
def default_final_states():
    return {2, 3}


@pytest.mark.parametrize(
    "start,final",
    [
        (None, None),
        ({1}, {2}),
        ({0, 2, 3}, {0, 2, 3}),
    ],
)
def test_nfa_is_equivalent(default_nfa, default_graph, start, final):
    if not start:
        start = {0, 1, 2, 3, 4}
    if not final:
        final = {0, 1, 2, 3, 4}

    nfa = default_nfa
    for state in start:
        nfa.add_start_state(State(state))
    for state in final:
        nfa.add_final_state(State(state))

    nfa_from_graph = transform_graph_to_nfa(default_graph, start, final)

    assert nfa_from_graph.is_equivalent_to(nfa)


def test_not_deterministic(default_graph):
    nfa = transform_graph_to_nfa(default_graph)
    return not nfa.is_deterministic()


@pytest.mark.parametrize(
    "word,expected_accept",
    [
        ("x", True),
        ("xxxx", True),
        ("xxy", True),
        ("", True),
        ("yyy", True),
        ("y", False),
        ("xx", False),
        ("xy", False),
    ],
)
def test_accepts_word(
    default_graph, default_start_states, default_final_states, word, expected_accept
):
    nfa = transform_graph_to_nfa(
        default_graph, default_start_states, default_final_states
    )

    assert nfa.accepts(word) == expected_accept


def test_mismatch_states(default_graph):
    with pytest.raises(AutomataException):
        transform_graph_to_nfa(default_graph, {0, 1, 2, 33}, {0, 1, 2, 3})


def test_null_graph():
    graph = nx.null_graph(create_using=nx.MultiDiGraph)
    nfa_from_graph = transform_graph_to_nfa(graph)

    assert nfa_from_graph.is_empty()


def test_empty_graph():
    graph = nx.empty_graph(2, create_using=nx.MultiDiGraph)
    nfa_from_graph = transform_graph_to_nfa(graph)

    nfa = NondeterministicFiniteAutomaton()
    nfa.add_start_state(State(0))
    nfa.add_start_state(State(1))
    nfa.add_final_state(State(0))
    nfa.add_final_state(State(1))

    assert nfa_from_graph.is_equivalent_to(nfa)


def test_one_node_loop_graph():
    graph = nx.empty_graph(1, create_using=nx.MultiDiGraph)
    graph.add_edge(0, 0, label="x")
    nfa_from_graph = transform_graph_to_nfa(graph)

    nfa = NondeterministicFiniteAutomaton()
    nfa.add_start_state(State(0))
    nfa.add_final_state(State(0))
    nfa.add_transition(State(0), Symbol("x"), State(0))

    assert nfa_from_graph.is_equivalent_to(nfa)
