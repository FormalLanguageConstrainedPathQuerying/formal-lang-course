import os

from networkx import MultiDiGraph
from networkx.drawing import nx_pydot
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State

from project.automaton_manager import AutomatonManager
from project.matrix_manager import MatrixManager


def load_expected_graph() -> MultiDiGraph:
    path = os.path.dirname(os.path.abspath(__file__)) + "/res/expected.dot"
    return nx_pydot.read_dot(path)


def test_transitive_closure():
    nfa = AutomatonManager.create_nfa_from_graph(load_expected_graph())

    boolean_matrix = MatrixManager.from_nfa_to_boolean_matrix(nfa)
    transitive_closure = MatrixManager.get_transitive_closure(boolean_matrix)

    assert transitive_closure.sum() == transitive_closure.size


def test_intersection():
    first_nfa = NondeterministicFiniteAutomaton()
    first_nfa.add_transitions(
        [(0, "a", 1), (0, "c", 1), (0, "c", 0), (1, "b", 1), (1, "c", 2), (2, "d", 0)]
    )
    first_nfa.add_start_state(State(0))
    first_nfa.add_final_state(State(0))
    first_nfa.add_final_state(State(1))
    first_nfa.add_final_state(State(2))

    second_nfa = NondeterministicFiniteAutomaton()
    second_nfa.add_transitions([(0, "a", 1), (0, "a", 0), (1, "b", 1), (1, "e", 2)])
    second_nfa.add_start_state(State(0))
    second_nfa.add_final_state(State(1))

    expected_nfa = first_nfa.get_intersection(second_nfa)

    first_matrix_automaton = MatrixManager.from_nfa_to_boolean_matrix(first_nfa)
    second_matrix_automaton = MatrixManager.from_nfa_to_boolean_matrix(second_nfa)
    intersected_fa = MatrixManager.intersect_two_nfa(
        first_matrix_automaton, second_matrix_automaton
    )

    actual_nfa = MatrixManager.from_boolean_matrix_to_nfa(intersected_fa)

    assert actual_nfa.is_equivalent_to(expected_nfa)
