import pytest
from pyformlang.finite_automaton import State, Symbol

from project.__init__ import *


@pytest.fixture()
def two_cycles_graph(request):
    return cfpq_data.labeled_two_cycles_graph(
        request.param[0], request.param[1], labels=(request.param[2], request.param[3])
    )


@pytest.fixture()
def dataset_graph():
    path_to_graph = cfpq_data.download("univ")
    return cfpq_data.graph_from_csv(path_to_graph)


@pytest.fixture()
def expected_dfa():
    dfa = DeterministicFiniteAutomaton()
    state0 = State(0)
    state1 = State(1)
    state2 = State(2)
    state3 = State(3)
    state4 = State(4)
    a = Symbol("a")
    c = Symbol("c")
    d = Symbol("d")
    e = Symbol("e")
    dfa.add_start_state(state0)
    dfa.add_final_state(state3)
    dfa.add_final_state(state4)
    dfa.add_transition(state0, a, state4)
    dfa.add_transition(state4, c, state4)

    dfa.add_transition(state0, d, state1)
    dfa.add_transition(state1, e, state2)
    dfa.add_transition(state2, d, state3)

    return dfa


@pytest.fixture()
def expected_nfa():
    exp_nfa = NondeterministicFiniteAutomaton()

    state0 = State(0)
    state1 = State(1)
    state2 = State(2)
    state3 = State(3)
    state4 = State(4)

    a = Symbol("a")
    b = Symbol("b")

    exp_nfa.add_start_state(state0)
    exp_nfa.add_final_state(state4)

    exp_nfa.add_transition(state0, a, state1)
    exp_nfa.add_transition(state0, b, state2)
    exp_nfa.add_transition(state1, a, state0)
    exp_nfa.add_transition(state4, b, state0)
    exp_nfa.add_transition(state3, b, state4)
    exp_nfa.add_transition(state2, b, state3)

    return exp_nfa
