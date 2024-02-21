from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State
from project.dfa import regex2dfa, graph2nfa
from project.graph import create_two_cycles_graph


def test_1():
    dfa = regex2dfa("(1|0)*")

    bin_dfa = DeterministicFiniteAutomaton()

    bin_dfa.add_start_state(State(0))
    bin_dfa.add_final_state(State(0))

    bin_dfa.add_transitions([(0, "1", 0), (0, "0", 0)])

    assert bin_dfa.is_equivalent_to(dfa)


def test_2():
    nfa = graph2nfa(create_two_cycles_graph(3, 3, ("1", "0")), [0], [0])
    dfa = regex2dfa("(1 1 1 1|0 0 0 0)*")
    assert dfa.is_equivalent_to(nfa)
