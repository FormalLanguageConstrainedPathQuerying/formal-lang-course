import cfpq_data
from pyformlang.finite_automaton import DeterministicFiniteAutomaton, EpsilonNFA
from pyformlang.regular_expression import Regex

from project.regex_utils import (
    regex_to_dfa,
    create_automaton,
    create_graph,
    create_nfa_from_graph,
)


def test_regex_to_graph_one_letter():
    dfa = regex_to_dfa(Regex("a"))
    expected = create_automaton(
        transitions=[(0, "a", 1)],
        start_states=[0],
        final_states=[1],
        automaton=DeterministicFiniteAutomaton(),
    )

    assert dfa.is_equivalent_to(expected)


def test_regex_to_graph_long_lable():
    dfa = regex_to_dfa(Regex("long_lable"))
    expected = create_automaton(
        transitions=[(0, "long_lable", 1)],
        start_states=[0],
        final_states=[1],
        automaton=DeterministicFiniteAutomaton(),
    )

    assert dfa.is_equivalent_to(expected)


def test_regex_to_graph_two_letter():
    dfa = regex_to_dfa(Regex("a b"))
    expected = create_automaton(
        transitions=[(0, "a", 1), (1, "b", 2)],
        start_states=[0],
        final_states=[2],
        automaton=DeterministicFiniteAutomaton(),
    )

    assert dfa.is_equivalent_to(expected)


def test_regex_to_graph_loop():
    dfa = regex_to_dfa(Regex("a*"))
    expected = create_automaton(
        transitions=[(0, "a", 0)],
        start_states=[0],
        final_states=[0],
        automaton=DeterministicFiniteAutomaton(),
    )

    assert dfa.is_equivalent_to(expected)


def test_create_nfa_from_graph_two_gen_cycle():
    graph = cfpq_data.labeled_two_cycles_graph(3, 2, labels=["a", "a"])
    automaton = create_nfa_from_graph(graph, start_states=[0], final_states=[2, 5])

    assert automaton.accepts("aa")
    assert not automaton.accepts("a")


def test_create_nfa_from_graph():
    automaton = create_nfa_from_graph(
        graph=create_graph([0, 1, 2], [(0, "a", 1), (0, "a", 2)]),
        start_states={0},
        final_states={1, 2},
    )

    expected = create_automaton(
        transitions=[(0, "a", 1), (0, "a", 2)],
        start_states=[0],
        final_states=[1, 2],
        automaton=EpsilonNFA(),
    )

    assert automaton.is_equivalent_to(expected)
