from typing import Iterable

import pytest
from pyformlang.finite_automaton import (
    Symbol,
    State,
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
)
from pyformlang.regular_expression import MisformedRegexError

from project import get_two_cycles, Graph
from project.automaton_tools import *


def test_wrong_regex() -> None:
    with pytest.raises(MisformedRegexError):
        get_min_dfa("*|wrong_regex|*")


def test_dfa() -> None:
    min_dfa = get_min_dfa("i* l* y* a* | 1901")

    assert min_dfa.is_deterministic()


def test_min_dfa() -> None:
    actual_dfa = get_min_dfa("i* l* y* a* | 1901")
    expected_min_dfa = actual_dfa.minimize()

    assert actual_dfa.is_equivalent_to(expected_min_dfa) and len(
        actual_dfa.states
    ) == len(expected_min_dfa.states)


@pytest.mark.parametrize(
    "actual_regex, expected_word, not_expected_word",
    [
        ("", [], [Symbol("*")]),
        (
            "i* l* y* a* | 1901",
            [Symbol("i"), Symbol("l"), Symbol("y"), Symbol("a")],
            [Symbol("i"), Symbol("l"), Symbol("y"), Symbol("a"), Symbol("1901")],
        ),
        (
            "(a | b)* 00* | 11*",
            [Symbol("a"), Symbol("a"), Symbol("00"), Symbol("00"), Symbol("00")],
            [Symbol("a"), Symbol("b"), Symbol("11")],
        ),
    ],
)
def test_min_dfa_accepts(
    actual_regex: str,
    expected_word: Iterable[Symbol],
    not_expected_word: Iterable[Symbol],
) -> None:
    actual_min_dfa = get_min_dfa(actual_regex)

    if actual_regex == "":
        assert actual_min_dfa.is_empty()
    else:
        assert actual_min_dfa.accepts(expected_word) and not actual_min_dfa.accepts(
            not_expected_word
        )


def test_get_min_dfa() -> None:
    expected_min_dfa = DeterministicFiniteAutomaton()

    state_0 = State(0)
    state_1 = State(1)
    state_2 = State(2)
    state_3 = State(3)

    symbol_i = Symbol("i")
    symbol_l = Symbol("l")
    symbol_y = Symbol("y")
    symbol_a = Symbol("a")

    expected_min_dfa.add_start_state(state_0)

    expected_min_dfa.add_final_state(state_0)
    expected_min_dfa.add_final_state(state_1)
    expected_min_dfa.add_final_state(state_2)
    expected_min_dfa.add_final_state(state_3)

    expected_min_dfa.add_transition(state_0, symbol_i, state_0)
    expected_min_dfa.add_transition(state_0, symbol_l, state_1)
    expected_min_dfa.add_transition(state_0, symbol_y, state_2)
    expected_min_dfa.add_transition(state_0, symbol_a, state_3)

    expected_min_dfa.add_transition(state_1, symbol_l, state_1)
    expected_min_dfa.add_transition(state_1, symbol_y, state_2)
    expected_min_dfa.add_transition(state_1, symbol_a, state_3)

    expected_min_dfa.add_transition(state_2, symbol_y, state_2)
    expected_min_dfa.add_transition(state_2, symbol_a, state_3)

    expected_min_dfa.add_transition(state_3, symbol_a, state_3)

    actual_min_dfa = get_min_dfa("i* l* y* a*")

    assert actual_min_dfa.is_equivalent_to(expected_min_dfa) and len(
        actual_min_dfa.states
    ) == len(expected_min_dfa.states)


def two_cycles_graph() -> Graph:
    return get_two_cycles(2, 2)


def without_nodes_graph() -> Graph:
    without_nodes = two_cycles_graph()
    without_nodes.graph.remove_nodes_from(list(without_nodes.graph.nodes))
    without_nodes.description.set_name("without_nodes")

    return without_nodes


def without_edges_graph() -> Graph:
    without_edges = two_cycles_graph()
    without_edges.graph.remove_edges_from(list(without_edges.graph.edges))
    without_edges.description.set_name("without_edges")

    return without_edges


def one_node_graph() -> Graph:
    one_node = two_cycles_graph()
    [one_node.graph.remove_node(node) for node in range(1, one_node.description.nodes)]
    one_node.graph.add_edge(0, 0, label="x")
    one_node.description.set_name("one_node")

    return one_node


def two_cycles_expected_nfa() -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton()
    nfa.add_transitions(
        [(0, "a", 1), (1, "a", 2), (2, "a", 0), (0, "b", 3), (3, "b", 4), (4, "b", 0)]
    )

    return nfa


def without_nodes_expected_nfa() -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton()

    return nfa


def without_edges_expected_nfa() -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton()
    [nfa.states.add(State(node)) for node in without_edges_graph().graph.nodes]

    return nfa


def one_node_expected_nfa() -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton()
    state = State(0)
    symbol = Symbol("x")
    nfa.add_transition(state, symbol, state)

    return nfa


@pytest.mark.parametrize(
    "graph",
    [
        two_cycles_graph(),
        without_nodes_graph(),
        without_edges_graph(),
        one_node_graph(),
    ],
)
def test_wrong_states(graph) -> None:
    with pytest.raises(ValueError):
        get_nfa(graph.graph, {0, 4, 199}, {-9, 3, 19})


@pytest.mark.parametrize(
    "graph",
    [
        two_cycles_graph(),
        without_nodes_graph(),
        without_edges_graph(),
        one_node_graph(),
    ],
)
def test_nfa(graph) -> None:
    nfa = get_nfa(graph.graph)

    assert isinstance(nfa, NondeterministicFiniteAutomaton)


@pytest.mark.parametrize(
    "graph, expected_word, not_expected_word",
    [
        (two_cycles_graph(), "", "epsilon"),
        (two_cycles_graph(), "aaa", "baba"),
        (two_cycles_graph(), "bbb", " "),
        (two_cycles_graph(), "bbbbbb", "aaababa"),
        (two_cycles_graph(), "aaabbbaaa", " ab "),
        (without_nodes_graph(), "", "epsilon"),
        (without_edges_graph(), "", "epsilon"),
        (one_node_graph(), "xxx", "epsilon"),
    ],
)
def test_nfa_accepts(graph, expected_word, not_expected_word) -> None:
    actual_nfa = get_nfa(graph.graph)

    if graph.graph.number_of_nodes() == 0:
        assert actual_nfa.is_empty()
    else:
        assert actual_nfa.accepts(expected_word) and not actual_nfa.accepts(
            not_expected_word
        )


@pytest.mark.parametrize(
    "graph, expected_ndfa, start_states, final_states",
    [
        (two_cycles_graph(), two_cycles_expected_nfa(), {0}, {3}),
        (two_cycles_graph(), two_cycles_expected_nfa(), {0}, {1, 4}),
        (two_cycles_graph(), two_cycles_expected_nfa(), {2, 3}, {0}),
        (two_cycles_graph(), two_cycles_expected_nfa(), {0, 1, 2}, {0, 3, 4}),
        (two_cycles_graph(), two_cycles_expected_nfa(), None, None),
        (without_nodes_graph(), without_nodes_expected_nfa(), None, None),
        (without_edges_graph(), without_edges_expected_nfa(), {3}, None),
        (one_node_graph(), one_node_expected_nfa(), {0}, {0}),
    ],
)
def test_get_nfa(graph, expected_ndfa, start_states, final_states) -> None:
    if graph.graph.number_of_nodes() == 0:
        actual_nfa = get_nfa(graph.graph, start_states, final_states)

        assert actual_nfa.is_empty() == expected_ndfa.is_empty()
    else:
        if not start_states:
            start_states = set(range(graph.graph.number_of_nodes()))

        for state in start_states:
            expected_ndfa.add_start_state(State(state))

        if not final_states:
            final_states = set(range(graph.graph.number_of_nodes()))

        for state in final_states:
            expected_ndfa.add_final_state(State(state))

        actual_nfa = get_nfa(graph.graph, start_states, final_states)

        assert actual_nfa.is_equivalent_to(expected_ndfa)
