from project import adjacency_matrix_fa as adj_m
from pyformlang.finite_automaton import DeterministicFiniteAutomaton


def test_is_empty():
    test_fa = DeterministicFiniteAutomaton()
    test_fa.add_start_state(0)
    test_fa.add_start_state(1)
    test_fa.add_start_state(2)
    test_fa.add_final_state(3)
    test_fa.add_final_state(4)
    test_fa.add_final_state(5)
    test_fa.add_transition(0, "a", 1)
    test_fa.add_transition(1, "a", 2)
    test_fa.add_transition(2, "a", 0)
    test_fa.add_transition(3, "b", 4)
    test_fa.add_transition(4, "b", 5)
    test_fa.add_transition(5, "b", 3)
    adjacency_matrix = adj_m.AdjacencyMatrixFA(test_fa)
    assert adjacency_matrix.is_empty()


def test_intersect_automata():
    dfa_from_lecture_1 = DeterministicFiniteAutomaton()
    dfa_from_lecture_1.add_start_state(0)
    dfa_from_lecture_1.add_start_state(1)
    dfa_from_lecture_1.add_transition(0, "a", 1)
    dfa_from_lecture_2 = DeterministicFiniteAutomaton()
    dfa_from_lecture_2.add_start_state(0)
    dfa_from_lecture_2.add_start_state(1)
    dfa_from_lecture_2.add_start_state(2)
    dfa_from_lecture_2.add_transition(0, "a", 1)
    dfa_from_lecture_2.add_transition(1, "a", 2)
    matrix1 = adj_m.AdjacencyMatrixFA(dfa_from_lecture_1)
    matrix2 = adj_m.AdjacencyMatrixFA(dfa_from_lecture_2)
    intersection = adj_m.intersect_automata(matrix1, matrix2)
    bool_matrix_for_a_elem = intersection.bool_decomposition["a"]
    assert bool_matrix_for_a_elem[0, 4]
    assert bool_matrix_for_a_elem[1, 5]
