from pyformlang.finite_automaton import EpsilonNFA

from project.t2_finite_automata import *
from project.t3_boolean_matrix_automata import BooleanMatrixAutomata


def test_intersect_two_automata():
    nfa1 = EpsilonNFA()
    nfa1.add_start_state(State(0))
    nfa1.add_final_state(State(0))
    nfa1.add_transitions([(0, "a", 1), (0, "b", 1), (1, "b", 0)])
    bma1 = BooleanMatrixAutomata(nfa1)

    nfa2 = EpsilonNFA()
    nfa2.add_start_state(State(0))
    nfa2.add_final_state(State(2))
    nfa2.add_transitions([(0, "a", 1), (1, "b", 2), (2, "b", 0), (0, "b", 2)])
    bma2 = BooleanMatrixAutomata(nfa2)
    actual_intersected_bma = bma1.intersect(bma2)
    actual_intersected_nfa = actual_intersected_bma.create_nfa_from_boolean_matrix()

    expected_intersected_nfa = EpsilonNFA()
    expected_intersected_nfa.add_start_state(State(0))
    expected_intersected_nfa.add_final_state(State(2))
    expected_intersected_nfa.add_transitions(
        [
            (0, "b", 5),
            (1, "b", 5),
            (2, "b", 3),
            (3, "b", 2),
            (4, "b", 2),
            (5, "b", 0),
            (0, "a", 4),
        ]
    )
    assert actual_intersected_nfa == expected_intersected_nfa
