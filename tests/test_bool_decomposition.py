from typing import Set, Tuple
from pyformlang.finite_automaton import State, Symbol, NondeterministicFiniteAutomaton
from scipy.sparse import dok_matrix
from project.utils.bool_decomposition import BoolDecompositionOfFA


def create_automaton(
    start_states: Set[State],
    final_states: Set[State],
    transitions: Set[Tuple[State, Symbol, State]],
) -> NondeterministicFiniteAutomaton:
    automaton = NondeterministicFiniteAutomaton()

    for state in start_states:
        automaton.add_start_state(state)
    for state in final_states:
        automaton.add_final_state(state)
    for transition in transitions:
        automaton.add_transition(*transition)

    return automaton


def test_from_fa():
    state1, state2, state3 = State(1), State(2), State(3)
    symbol_a, symbol_b = Symbol("a"), Symbol("b")
    automaton = create_automaton(
        start_states={state1},
        final_states={state3},
        transitions={
            (state1, symbol_a, state2),
            (state2, symbol_b, state3),
            (state3, symbol_a, state3),
            (state3, symbol_a, state1),
        },
    )
    bool_automaton = BoolDecompositionOfFA.from_fa(automaton)

    assert bool_automaton.start_states == {State(1)}
    assert bool_automaton.final_states == {State(3)}
    assert bool_automaton.matrices["a"].nnz == 3
    assert bool_automaton.matrices["a"][0, 1]
    assert bool_automaton.matrices["a"][2, 2]
    assert bool_automaton.matrices["a"][2, 0]
    assert bool_automaton.matrices["b"].nnz == 1
    assert bool_automaton.matrices["b"][1, 2]


def test_to_nfa():
    bool_automaton = BoolDecompositionOfFA(
        matrices={
            "a": dok_matrix([[0, 1, 0], [0, 0, 0], [1, 0, 1]]),
            "b": dok_matrix([[0, 0, 0], [0, 0, 1], [0, 0, 0]]),
        },
        state_to_index={State(1): 0, State(2): 1, State(3): 2},
        index_to_state={0: State(1), 1: State(2), 2: State(3)},
        start_states={State(1)},
        final_states={State(3)},
    )
    nfa = bool_automaton.to_nfa()

    assert nfa.states == {State(1), State(2), State(3)}
    assert nfa.start_states == {State(1)}
    assert nfa.final_states == {State(3)}
    assert nfa.get_number_transitions() == 4
    for transition in [
        (State(1), Symbol("a"), State(2)),
        (State(2), Symbol("b"), State(3)),
        (State(3), Symbol("a"), State(3)),
        (State(3), Symbol("a"), State(1)),
    ]:
        assert transition in nfa


def test_intersection():
    state1, state2, state3, state4 = State(1), State(2), State(3), State(4)
    symbol_a, symbol_b, symbol_c = Symbol("a"), Symbol("b"), Symbol("c")

    automaton1 = create_automaton(
        start_states={state1, state2},
        final_states={state3},
        transitions={
            (state1, symbol_a, state2),
            (state1, symbol_b, state2),
            (state1, symbol_b, state3),
            (state2, symbol_b, state2),
            (state2, symbol_a, state3),
            (state3, symbol_b, state1),
        },
    )
    bool_automaton1 = BoolDecompositionOfFA.from_fa(automaton1)

    automaton2 = create_automaton(
        start_states={state1},
        final_states={state3, state4},
        transitions={
            (state1, symbol_a, state1),
            (state1, symbol_b, state3),
            (state3, symbol_c, state1),
            (state3, symbol_a, state3),
            (state3, symbol_b, state4),
            (state4, symbol_a, state1),
        },
    )
    bool_automaton2 = BoolDecompositionOfFA.from_fa(automaton2)

    intersection = BoolDecompositionOfFA.intersection(bool_automaton1, bool_automaton2)
    nfa = intersection.to_nfa()

    assert nfa.start_states == {State(0), State(3)}
    assert nfa.final_states == {State(7), State(8)}
    assert nfa.get_number_transitions() == 14
    for transition in [
        (State(0), symbol_a, State(3)),
        (State(1), symbol_a, State(4)),
        (State(2), symbol_a, State(3)),
        (State(3), symbol_a, State(6)),
        (State(4), symbol_a, State(7)),
        (State(5), symbol_a, State(6)),
        (State(0), symbol_b, State(4)),
        (State(1), symbol_b, State(5)),
        (State(0), symbol_b, State(7)),
        (State(0), symbol_b, State(7)),
        (State(3), symbol_b, State(4)),
        (State(4), symbol_b, State(5)),
        (State(6), symbol_b, State(1)),
        (State(7), symbol_b, State(2)),
    ]:
        assert transition in nfa


def test_transitive_closure():
    bool_decomposition = BoolDecompositionOfFA(
        matrices={
            "a": dok_matrix([[1, 0, 0, 0], [0, 1, 0, 0], [1, 0, 1, 0], [0, 1, 0, 0]]),
            "b": dok_matrix([[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
        }
    )
    transitive_closure = bool_decomposition.transitive_closure()

    assert transitive_closure == {
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1),
        (2, 0),
        (2, 2),
        (3, 1),
        (3, 0),
        (2, 1),
    }
