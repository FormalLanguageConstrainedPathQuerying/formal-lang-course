from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    State,
    DeterministicFiniteAutomaton,
)

from project.boolean_decompositon import (
    get_intersect_boolean_decomposition,
    decomposition_to_automaton,
)
from project.rpq import (
    BooleanDecomposition,
)


def test_intersection():
    fa1 = NondeterministicFiniteAutomaton()
    fa1.add_transitions(
        [(0, "a", 1), (0, "b", 1), (0, "c", 0), (1, "b", 1), (1, "c", 2), (2, "d", 0)]
    )
    fa1.add_start_state(State(0))
    fa1.add_final_state(State(0))
    fa1.add_final_state(State(1))
    fa1.add_final_state(State(2))

    decomposition1 = BooleanDecomposition(fa1)

    fa2 = NondeterministicFiniteAutomaton()
    fa2.add_transitions([(0, "a", 1), (0, "a", 0), (1, "b", 1), (1, "e", 2)])
    fa2.add_start_state(State(0))
    fa2.add_final_state(State(1))

    decomposition2 = BooleanDecomposition(fa2)

    expected = DeterministicFiniteAutomaton()
    expected.add_transitions([(0, "a", 1), (1, "b", 1)])
    expected.add_start_state(State(0))
    expected.add_final_state(State(1))

    intersected = get_intersect_boolean_decomposition(decomposition1, decomposition2)

    fa = decomposition_to_automaton(intersected)

    assert fa.is_equivalent_to(expected)


def test_intersection_with_empty():
    fa1 = NondeterministicFiniteAutomaton()
    fa1.add_transitions(
        [(0, "a", 1), (0, "b", 1), (0, "c", 0), (1, "b", 1), (1, "c", 2), (2, "d", 0)]
    )
    fa1.add_start_state(State(0))
    fa1.add_final_state(State(0))
    fa1.add_final_state(State(1))
    fa1.add_final_state(State(2))

    decomposition1 = BooleanDecomposition(fa1)

    fa2 = NondeterministicFiniteAutomaton()

    decomposition2 = BooleanDecomposition(fa2)

    expected = DeterministicFiniteAutomaton()

    intersected = get_intersect_boolean_decomposition(decomposition1, decomposition2)

    fa = decomposition_to_automaton(intersected)

    assert fa.to_networkx().__str__() == expected.to_networkx().__str__()
