from project.automata_builder.DFA_builder import build_mdfa
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton


def test_build_mdfa():
    input = "a.(b|c*)*"
    mdfa = build_mdfa(input)

    expected = NondeterministicFiniteAutomaton()
    expected.add_start_state(0)
    expected.add_final_state(1)
    expected.add_transitions([(0, "a", 1), (1, "b", 1), (1, "c", 1)])

    assert mdfa.is_deterministic()
    assert mdfa.minimize().is_equivalent_to(mdfa)
    assert mdfa.is_equivalent_to(expected)
    assert len(mdfa.states) == len(expected.states)
    assert mdfa.get_number_transitions() == expected.get_number_transitions()
