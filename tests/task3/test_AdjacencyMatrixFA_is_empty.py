from project.task3 import AdjacencyMatrixFA
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton


def test_not_empty_fa():
    fa = NondeterministicFiniteAutomaton()
    fa.add_transitions([(0, "a", 1), (0, "b", 2), (1, "c", 2), (1, "a", 0)])
    fa.add_start_state(0)
    fa.add_final_state(2)

    amf = AdjacencyMatrixFA(fa)
    assert not amf.is_empty()


def test_empty_fa():
    fa = NondeterministicFiniteAutomaton()
    fa.add_transitions([(0, "a", 1), (0, "b", 2), (1, "c", 2), (1, "a", 0)])
    fa.add_start_state(2)
    fa.add_final_state(0)

    amf = AdjacencyMatrixFA(fa)
    assert amf.is_empty()
