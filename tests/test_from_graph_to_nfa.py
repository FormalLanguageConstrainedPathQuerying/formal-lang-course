import pytest
from pyformlang.finite_automaton import EpsilonNFA, NondeterministicFiniteAutomaton

from project.graph_utils import from_graph_to_nfa
from tests.test_utils import create_automata, create_graph

testdata = [
    (
        from_graph_to_nfa(
            graph=create_graph([0, 1], [(0, "ab", 1)]),
            start_states=[0],
            final_states=[1],
        ),
        create_automata(
            transitions=[(0, "ab", 1)],
            start_states=[0],
            final_states=[1],
            automata=EpsilonNFA(),
        ),
    ),
    (
        from_graph_to_nfa(graph=create_graph([0], [(0, "ab", 0)])),
        create_automata(
            transitions=[(0, "ab", 0)],
            start_states=[0],
            final_states=[0],
            automata=EpsilonNFA(),
        ),
    ),
    (
        from_graph_to_nfa(
            graph=create_graph([0, 1], [(0, "ab", 1), (1, "c", 1)]),
            start_states=[0],
            final_states=[1],
        ),
        create_automata(
            transitions=[(0, "ab", 1), (1, "c", 1)],
            start_states=[0],
            final_states=[1],
            automata=EpsilonNFA(),
        ),
    ),
    (
        from_graph_to_nfa(
            graph=create_graph([0, 1, 2], [(0, "a", 1), (0, "b", 2)]),
            start_states=[0],
            final_states=[1, 2],
        ),
        create_automata(
            transitions=[(0, "a", 1), (0, "b", 2)],
            start_states=[0],
            final_states=[1, 2],
            automata=EpsilonNFA(),
        ),
    ),
]


@pytest.mark.parametrize("actual,expected", testdata)
def test_from_graph_to_nfa(actual: EpsilonNFA, expected: EpsilonNFA):
    assert actual.is_equivalent_to(expected)
