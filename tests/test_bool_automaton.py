from pyformlang.finite_automaton import State

from project.__init__ import *


def test_intersect(expected_dfa, expected_nfa):
    """
    expected_dfa
       0   1   2   3   4
    0 { } {d} { } { } {a}
    1 { } { } {e} { } { }
    2 { } { } { } {d} { }
    3 { } { } { } { } { }
    4 { } { } { } { } {c}
    """

    """
    expected_nfa
       0   1   2   3   4
    0 { } {a} {b} { } { }
    1 {a} { } { } { } { }
    2 { } { } { } {b} { }
    3 { } { } { } { } {b}
    4 {b} { } { } { } { }
    """

    res_of_intersection_fa = NondeterministicFiniteAutomaton()
    res_of_intersection_fa.add_transitions([(0, "a", 21), (1, "a", 20)])
    res_of_intersection_fa.add_start_state(State(0))
    res_of_intersection_fa.add_final_state(State(19))
    res_of_intersection_fa.add_final_state(State(24))

    actual_intersection = BoolAutomaton(expected_dfa).intersect(
        BoolAutomaton(expected_nfa)
    )
    expected_intersection = BoolAutomaton(res_of_intersection_fa)

    for label in actual_intersection.edges.keys():
        assert (
            actual_intersection.edges.get(label).nnz
            == expected_intersection.edges.get(label).nnz
        )
    assert actual_intersection.start_states == expected_intersection.start_states
    assert actual_intersection.final_states == expected_intersection.final_states
