from pyformlang.finite_automaton import EpsilonNFA, Symbol, Epsilon, State

from project.automata import *
from tests.utils import *


def test_empty_graph_to_epsilon_nfa():
    empty_graph = MultiDiGraph()
    epsilon_nfa = graph_to_epsilon_nfa(
        graph=empty_graph,
        start_states=None,
        final_states=None,
    )
    assert not epsilon_nfa.states


def test_graph_to_epsilon_nfa():
    graph = MultiDiGraph()
    edges = [
        (0, 1, "b"),
        (0, 2, "a"),
        (1, 3, None),
        (1, 4, None),
        (0, 5, "abc"),
    ]

    for node_from, node_to, label in edges:
        graph.add_edge(node_from, node_to, label=label)
    epsilon_nfa = graph_to_epsilon_nfa(graph, start_states=None, final_states={1, 5})

    expected_epsilon_nfa = EpsilonNFA()
    transitions = [
        (State(0), Symbol("b"), State(1)),
        (State(0), Symbol("a"), State(2)),
        (State(1), Epsilon(), State(3)),
        (State(1), Epsilon(), State(4)),
        (State(0), Symbol("abc"), State(5)),
    ]
    for state_from, symbol, state_to in transitions:
        expected_epsilon_nfa.add_transition(state_from, symbol, state_to)
    for state in map(State, [0, 1, 2, 3, 4, 5]):
        expected_epsilon_nfa.add_start_state(State(state))
    for state in map(State, [1, 5]):
        expected_epsilon_nfa.add_final_state(State(state))

    assert check_automatons_are_equivalent(
        first_automaton=epsilon_nfa,
        second_automaton=expected_epsilon_nfa,
    )
