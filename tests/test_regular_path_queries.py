from pyformlang.finite_automaton import State

from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, Symbol
from pyformlang.regular_expression import Regex

from project import regular_path_queries as rpq, graph_utils, fsm

def get_sample_fa():
    states = [State(0), State(1)]
    fa = NondeterministicFiniteAutomaton()
    fa.add_start_state(states[0])
    fa.add_final_state(states[1])
    fa.add_transitions(
        [
            (states[0], Symbol("a"), states[0]),
            (states[1], Symbol("b"), states[0]),
            (states[0], Symbol("a"), states[1]),
        ]
    )
    return fa

def get_sampel_fa2():
    states = [State(0), State(1), State(2), State(3)]
    fa = NondeterministicFiniteAutomaton()
    fa.add_start_state(states[2])
    fa.add_start_state(states[3])
    fa.add_final_state(states[0])
    fa.add_final_state(states[1])
    fa.add_transitions(
        [
            (states[0], Symbol("a"), states[2]),
            (states[1], Symbol("a"), states[0]),
            (states[3], Symbol("a"), states[0]),
            (states[0], Symbol("b"), states[0]),
            (states[2], Symbol("b"), states[2]),
        ]
    )
    return fa
def test_intersection_with_empty_fa():
    fa = get_sample_fa()
    empty_fa = NondeterministicFiniteAutomaton()
    expected = fa.get_intersection(empty_fa)
    result = rpq.intersect(fa, empty_fa)
    assert expected.is_equivalent_to(result)

def test_self_intersection():
    fa = get_sampel_fa2()
    expected = fa.get_intersection(fa)
    result = rpq.intersect(fa, fa)
    assert expected.is_equivalent_to(result)

def test_intersection():
    fa = get_sampel_fa2()
    fa1 = get_sample_fa()
    expected = fa.get_intersection(fa1)
    result = rpq.intersect(fa, fa1)
    assert expected.is_equivalent_to(result)


