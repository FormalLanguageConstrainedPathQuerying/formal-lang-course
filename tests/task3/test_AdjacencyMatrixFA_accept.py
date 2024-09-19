from project.task3 import AdjacencyMatrixFA
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, Symbol

fa_1 = NondeterministicFiniteAutomaton()
fa_1.add_transitions([(0, "a", 1), (0, "b", 2), (1, "c", 2), (1, "a", 0)])
fa_1.add_start_state(0)
fa_1.add_final_state(2)

amf_1 = AdjacencyMatrixFA(fa_1)


def __str_to_symbols(word: str):
    return [Symbol(x) for x in word]


def test_accept():
    assert not amf_1.accepts(__str_to_symbols("aac"))
    assert amf_1.accepts(__str_to_symbols("aab"))
    assert not amf_1.accepts(__str_to_symbols("aaab"))
    assert amf_1.accepts(__str_to_symbols("aaac"))
    assert not amf_1.accepts(__str_to_symbols("c"))
    assert amf_1.accepts(__str_to_symbols("b"))
