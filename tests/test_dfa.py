from pyformlang.finite_automaton import DeterministicFiniteAutomaton, State
from project.task2 import regex_to_dfa, graph_to_nfa
from project.task1 import create_two_cycles_graph


def test_1():
    dfa = regex_to_dfa("(1|0)*")

    bin_dfa = DeterministicFiniteAutomaton()

    bin_dfa.add_start_state(State(0))
    bin_dfa.add_final_state(State(0))

    bin_dfa.add_transitions([(0, "1", 0), (0, "0", 0)])

    assert bin_dfa.is_equivalent_to(dfa)


def test_2():
    nfa = graph_to_nfa(create_two_cycles_graph(3, 3, ("1", "0")), [0], [0])
    dfa = regex_to_dfa("(1 1 1 1|0 0 0 0)*")
    assert dfa.is_equivalent_to(nfa)

