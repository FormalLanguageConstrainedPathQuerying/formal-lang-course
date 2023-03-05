import project.finite_automaton_build as fab
import pyformlang.finite_automaton as fa
import project.graphs as gr
import cfpq_data as cd


def test_min_dfa1():
    # Declaration of the DFA
    dfa1 = fa.DeterministicFiniteAutomaton()

    # Creation of the states
    state0 = fa.State(0)
    state1 = fa.State(1)
    state2 = fa.State(2)
    state3 = fa.State(3)

    # Creation of the symbols
    symb_a = fa.Symbol("a")
    symb_b = fa.Symbol("b")
    symb_c = fa.Symbol("c")
    symb_d = fa.Symbol("d")

    # Add a start state
    dfa1.add_start_state(state0)

    # Add one final state
    dfa1.add_final_state(state3)

    # Create transitions
    dfa1.add_transition(state0, symb_a, state1)
    dfa1.add_transition(state1, symb_b, state2)
    dfa1.add_transition(state2, symb_c, state3)
    dfa1.add_transition(state2, symb_d, state3)

    regex = "($.((a.b).(d|c)))"
    dfa2 = fab.get_min_dfa_from_regex_str(regex)

    assert dfa1.accepts("abc")
    assert dfa1.accepts("abd")
    assert dfa2.accepts("abd")
    assert dfa2.accepts("abd")

    assert dfa1.is_equivalent_to(dfa2)


def test_min_dfa2():
    # Declaration of the DFA
    dfa1 = fa.DeterministicFiniteAutomaton()

    # Creation of the states
    state0 = fa.State(0)
    state1 = fa.State(1)
    state2 = fa.State(2)
    state3 = fa.State(3)

    # Creation of the symbols
    symb_a = fa.Symbol("a")
    symb_b = fa.Symbol("b")
    symb_c = fa.Symbol("c")
    symb_d = fa.Symbol("d")

    # Add a start state
    dfa1.add_start_state(state0)

    # Add two final states
    dfa1.add_final_state(state2)
    dfa1.add_final_state(state3)

    # Create transitions
    dfa1.add_transition(state0, symb_a, state1)
    dfa1.add_transition(state1, symb_b, state1)
    dfa1.add_transition(state1, symb_c, state2)
    dfa1.add_transition(state1, symb_d, state3)

    regex = "($.(a.((b)*.c)))|($.(a.((b)*.d)))"
    dfa2 = fab.get_min_dfa_from_regex_str(regex)

    assert dfa1.is_equivalent_to(dfa2)


def test_nfa1():
    g = cd.labeled_two_cycles_graph(2, 2)
    nfa = fab.get_nfa_from_graph(g, [1], [5])
