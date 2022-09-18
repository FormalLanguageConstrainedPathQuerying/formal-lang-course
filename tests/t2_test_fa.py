import cfpq_data
from networkx.algorithms import isomorphism
from pyformlang.finite_automaton import Symbol, NondeterministicFiniteAutomaton, State
from pyformlang.regular_expression import PythonRegex
from networkx import is_isomorphic

import project.t1_graph_module as gm
import project.t2_deterministic_finite_automata as fsm


def test_build_minimal_dfa_from_regex():
    regex = PythonRegex("a+[cd]")
    dfa = fsm.build_minimal_dfa_from_regex(regex)
    sa = Symbol("a")
    sc = Symbol("c")
    sd = Symbol("d")
    assert dfa.accepts([sa, sd])
    assert dfa.accepts([sa for _ in range(10)] + [sd])
    assert dfa.accepts([sa, sc])
    assert not dfa.accepts([sc])
    assert not dfa.accepts([sa, sc, sd])


def test_build_nfa_from_graph():
    graph = cfpq_data.labeled_two_cycles_graph(4, 6, labels=("a", "b"))
    nfa = fsm.build_nfa_from_graph(graph, [0], [10])
    sa = Symbol("a")
    sb = Symbol("b")
    assert nfa.accepts([sa for _ in range(5)] + [sb for _ in range(6)])
