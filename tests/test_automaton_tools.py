from typing import Iterable

import pytest
from pyformlang.cfg import CFG
from pyformlang.finite_automaton import (
    Symbol,
    State,
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
)
from pyformlang.regular_expression import MisformedRegexError, Regex

from project.automaton_tools import (
    RSMBox,
    get_min_dfa_from_regex,
    get_nfa_from_graph,
    get_rsm_from_ecfg,
    minimize_rsm,
)
from project.grammar_tools import ECFG, get_ecfg_from_cfg
from project.graph_tools import get_two_cycles, Graph


def test_wrong_regex() -> None:
    with pytest.raises(MisformedRegexError):
        get_min_dfa_from_regex(Regex("*|wrong_regex|*"))


def test_dfa() -> None:
    min_dfa = get_min_dfa_from_regex(Regex("i* l* y* a* | 1901"))

    assert min_dfa.is_deterministic()


def test_min_dfa() -> None:
    actual_dfa = get_min_dfa_from_regex(Regex("i* l* y* a* | 1901"))
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
    actual_min_dfa = get_min_dfa_from_regex(Regex(actual_regex))

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

    actual_min_dfa = get_min_dfa_from_regex(Regex("i* l* y* a*"))

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
        get_nfa_from_graph(graph.graph, {0, 4, 199}, {-9, 3, 19})


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
    nfa = get_nfa_from_graph(graph.graph)

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
    actual_nfa = get_nfa_from_graph(graph.graph)

    if graph.graph.number_of_nodes() == 0:
        assert actual_nfa.is_empty()
    else:
        assert actual_nfa.accepts(expected_word) and not actual_nfa.accepts(
            not_expected_word
        )


@pytest.mark.parametrize(
    "graph, expected_ndfa, start_node_nums, final_node_nums",
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
def test_get_nfa(graph, expected_ndfa, start_node_nums, final_node_nums) -> None:
    if graph.graph.number_of_nodes() == 0:
        actual_nfa = get_nfa_from_graph(graph.graph, start_node_nums, final_node_nums)

        assert actual_nfa.is_empty() == expected_ndfa.is_empty()
    else:
        if not start_node_nums:
            start_node_nums = set(graph.graph.nodes)

        for start_node in start_node_nums:
            expected_ndfa.add_start_state(State(start_node))

        if not final_node_nums:
            final_node_nums = set(graph.graph.nodes)

        for final_node in final_node_nums:
            expected_ndfa.add_final_state(State(final_node))

        actual_nfa = get_nfa_from_graph(graph.graph, start_node_nums, final_node_nums)

        assert actual_nfa.is_equivalent_to(expected_ndfa)


@pytest.mark.parametrize(
    """cfg_text""",
    (
        """

            """,
        """
            S -> S b
            S -> epsilon
            """,
        """
            S -> a S b S
            S -> epsilon
            S -> B B
            A -> C
            C -> A B C
            """,
    ),
)
def test_rsm_from_cfg(cfg_text):
    ecfg = get_ecfg_from_cfg(CFG.from_text(cfg_text))
    rsm = get_rsm_from_ecfg(ecfg)

    actual_start_symbol = rsm.start_symbol
    expected_start_symbol = ecfg.start_symbol

    actual_boxes = rsm.boxes
    expected_boxes = [
        RSMBox(production.head, get_min_dfa_from_regex(production.body))
        for production in ecfg.productions
    ]

    return (
        actual_start_symbol == expected_start_symbol and actual_boxes == expected_boxes
    )


@pytest.mark.parametrize(
    """ecfg_text""",
    (
        """

                """,
        """
                S -> S G
                G -> epsilon
                """,
        """
                S -> a A b C
                A -> C
                C -> A B C
                """,
    ),
)
def test_rsm_from_ecfg_is_minimal(ecfg_text):
    ecfg = ECFG.from_text(ecfg_text)
    rsm = get_rsm_from_ecfg(ecfg)
    min_rsm = minimize_rsm(rsm)

    assert rsm == min_rsm
