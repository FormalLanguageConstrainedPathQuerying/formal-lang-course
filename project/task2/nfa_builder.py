from networkx import MultiDiGraph
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State
from pyformlang.finite_automaton import Symbol


def add_transitions(nfa, graph):
    nfa.add_transitions(
        {
            (State(u), Symbol(label), State(v))
            for u, v, label in graph.edges.data("label")
        }
    )


def add_start_states(nfa, start_states, nodes):
    if not start_states.issubset(nodes):
        raise ValueError("Nodes are not subset of graph")
    for node in start_states:
        nfa.add_start_state(State(node))


def add_final_states(nfa, final_states, nodes):
    if not final_states.issubset(nodes):
        raise ValueError("Nodes are not subset of graph")
    for node in final_states:
        nfa.add_final_state(State(node))


def graph_to_nfa(
    graph: MultiDiGraph, start_states: set[int], final_states: set[int]
) -> NondeterministicFiniteAutomaton:
    """
    Generate nondeterministic finite automaton by graph with given start and finale states

    :param graph:  graph that would be base for automata
    :param start_states: set of vertexes that would be start states
    :param final_states:  set of vertexes that would be finale states
    :return:
    """

    nfa = NondeterministicFiniteAutomaton()
    nodes = set(graph)

    if not start_states:
        start_states = nodes
    if not final_states:
        final_states = nodes

    add_transitions(nfa, graph)
    add_start_states(nfa, start_states, nodes)
    add_final_states(nfa, final_states, nodes)

    return nfa
