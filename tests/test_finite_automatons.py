from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
import project.finite_automatons as fa
import project.graphs as graphs
import pytest


def test_regex_dfa():
    dfa = fa.regex_to_dfa("abc (abc* def*)*")

    expected = NondeterministicFiniteAutomaton()
    expected.add_start_state(0)
    expected.add_final_state(1)
    expected.add_transitions([(0, "abc", 1), (1, "abc", 1), (1, "def", 1)])

    assert expected.is_equivalent_to(dfa)


@pytest.mark.parametrize(
    "regex_str",
    ["abc def", "abc|def", "abc def | def abc", "abc def*", "abc* def", "(abc* def*)*"],
)
def test_regex_dfa_minimal(regex_str: str):
    dfa = fa.regex_to_dfa(regex_str)
    assert dfa.is_deterministic()
    minimal = dfa.minimize()
    assert dfa.is_equivalent_to(minimal)
    assert len(minimal.states) == len(dfa.states)
    assert minimal.get_number_transitions() == dfa.get_number_transitions()


def test_graph_nfa():
    g = graphs.make_two_cycles(3, 4)
    nfa = fa.graph_to_nfa(g)
    expected = NondeterministicFiniteAutomaton(range(6))
    for i in range(3):
        j = (i + 1) % 3
        expected.add_transition(i, "a", j)
    for i in range(4):
        j = (i + 1) % 4
        expected.add_transition(2 + i, "b", 2 + j)
    assert expected.is_equivalent_to(nfa)
