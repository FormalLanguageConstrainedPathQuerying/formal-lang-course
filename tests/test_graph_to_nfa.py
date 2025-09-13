import pytest
import networkx as nx
from pyformlang.finite_automaton import State, Symbol
from project import t2_fa_utils as t2


def test_empty_graph():
    G = nx.MultiDiGraph()
    nfa = t2.graph_to_nfa(G)

    assert len(nfa.states) == 0
    assert len(nfa.to_dict()) == 0


def test_single_edge_with_label():
    G = nx.MultiDiGraph()
    G.add_edge(0, 1, label="a")

    nfa = t2.graph_to_nfa(G, start_states={0}, final_states={1})

    assert State(0) in nfa.start_states
    assert State(1) in nfa.final_states

    transitions = nfa.to_dict()
    assert State(0) in transitions
    assert Symbol("a") in transitions[State(0)]
    assert State(1) in transitions[State(0)][Symbol("a")]


def test_all_nodes_start_and_final_if_not_specified():
    G = nx.MultiDiGraph()
    G.add_edge(0, 1, label="a")
    G.add_edge(1, 2, label="b")

    nfa = t2.graph_to_nfa(G)

    assert all(State(v) in nfa.start_states for v in G.nodes)
    assert all(State(v) in nfa.final_states for v in G.nodes)


@pytest.mark.parametrize("attr_name", ["label", "symbol", "weight"])
def test_edge_labels_from_different_attrs(attr_name):
    G = nx.MultiDiGraph()
    G.add_edge(0, 1, **{attr_name: "x"})

    nfa = t2.graph_to_nfa(G, start_states={0}, final_states={1})

    transitions = nfa.to_dict()
    assert Symbol("x") in transitions[State(0)]
    assert State(1) in transitions[State(0)][Symbol("x")]


def test_epsilon_transition_when_no_label():
    G = nx.MultiDiGraph()
    G.add_edge(0, 1)

    nfa = t2.graph_to_nfa(G, start_states={0}, final_states={1})

    transitions = nfa.to_dict()
    assert None in transitions[State(0)]
    assert State(1) in transitions[State(0)][None]


def test_multi_edges_between_same_nodes():
    G = nx.MultiDiGraph()
    G.add_edge(0, 1, label="a")
    G.add_edge(0, 1, label="b")

    nfa = t2.graph_to_nfa(G, start_states={0}, final_states={1})

    transitions = nfa.to_dict()
    assert Symbol("a") in transitions[State(0)]
    assert Symbol("b") in transitions[State(0)]
    assert State(1) in transitions[State(0)][Symbol("a")]
    assert State(1) in transitions[State(0)][Symbol("b")]
