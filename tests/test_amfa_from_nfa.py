import numpy as np
import pytest
import random
from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    State,
    Symbol,
)
from project import t3_graph_fa as t3


def make_simple_nfa(set_transactions):
    nfa = NondeterministicFiniteAutomaton()
    q0, q1 = State("q0"), State("q1")
    a, b = Symbol("a"), Symbol("b")

    nfa.add_start_state(q0)
    nfa.add_final_state(q1)
    if set_transactions:
        nfa.add_transition(q0, a, q1)  # q0 -a-> q1
        nfa.add_transition(q1, b, q0)  # q1 -b-> q0

    return nfa


def make_random_nfa(
    alphabet, n_states, start_states_num, final_states_num, transitions_num=None
):
    nfa = NondeterministicFiniteAutomaton()

    states = [State(f"q{i}") for i in range(n_states)]

    start_states = random.sample(states, k=start_states_num)
    for s in start_states:
        nfa.add_start_state(s)

    final_states = random.sample(states, k=final_states_num)
    for f in final_states:
        nfa.add_final_state(f)

    if transitions_num is None:
        transitions_num = n_states * len(alphabet)

    if transitions_num == 0:
        return nfa

    for _ in range(transitions_num):
        s_from = random.choice(states)
        s_to = random.choice(states)
        sym = random.choice(alphabet)
        nfa.add_transition(s_from, sym, s_to)

    return nfa


def test_from_pyformlang_nfa():
    nfa = make_simple_nfa(True)
    fa = t3.AdjacencyMatrixFA(nfa)

    assert fa.n_states == 2

    assert fa.start_states.tolist() == [True, False] or fa.start_states.tolist() == [
        False,
        True,
    ]
    assert fa.final_states.sum() == 1

    mat_a = fa.transitions["a"].toarray()
    assert mat_a.sum() == 1
    assert (mat_a == np.array([[0, 1], [0, 0]], dtype=bool)).any()

    mat_b = fa.transitions["b"].toarray()
    assert mat_b.sum() == 1
    assert (mat_b == np.array([[0, 0], [1, 0]], dtype=bool)).any()


@pytest.mark.parametrize(
    "nfa, is_empty_truth",
    [
        (make_simple_nfa(False), True),
        (make_random_nfa(["a", "b", "c", "d"], 4, 1, 1, 0), True),
        (make_random_nfa(["a"], 4, 4, 4, 0), False),
        (make_random_nfa([], 1, 1, 1, 0), False),
        (make_random_nfa(["a"], 1, 1, 1, 1), False),
    ],
)
def test_am_emptyness(nfa, is_empty_truth):
    fa = t3.AdjacencyMatrixFA(nfa)
    assert fa.is_empty() == is_empty_truth


def test_accepts_simple_words():
    nfa = make_simple_nfa(True)
    fa = t3.AdjacencyMatrixFA(nfa)

    a, b = Symbol("a"), Symbol("b")

    assert fa.accepts([a]) is True
    assert fa.accepts([a, b]) is False
    assert fa.accepts([b]) is False
    assert fa.accepts([b, a]) is False
    assert fa.accepts([]) is False


def test_accepts_with_cycle():
    nfa = make_simple_nfa(True)
    fa = t3.AdjacencyMatrixFA(nfa)

    a, b = Symbol("a"), Symbol("b")

    assert fa.accepts([a, b, a]) is True
    assert fa.accepts([a, b, a, b]) is False
    assert fa.accepts([a, b, a, b, a]) is True
    assert fa.accepts([a, b, a, b, b, b, a]) is False
    assert fa.accepts([a, b, a, b, b]) is False


def test_accepts_empty_nfa():
    nfa = make_simple_nfa(False)
    fa = t3.AdjacencyMatrixFA(nfa)

    a, b = Symbol("a"), Symbol("b")
    assert fa.accepts([a]) is False
    assert fa.accepts([b]) is False
    assert fa.accepts([]) is False
