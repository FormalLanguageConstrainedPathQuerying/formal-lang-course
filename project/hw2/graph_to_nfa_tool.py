from typing import Set, Tuple

from networkx import MultiDiGraph
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State
from dataclasses import dataclass
import cfpq_data
import networkx


@dataclass
class Graph:
    edges_cnt: int
    nodes_cnt: int
    labels: Set


def load_graph(graph_name: str):
    path = cfpq_data.download(graph_name)
    graph = cfpq_data.graph_from_csv(path)
    edges_cnt = graph.number_of_edges()
    nodes_cnt = graph.number_of_nodes()
    labels = cfpq_data.get_sorted_labels(graph)
    return Graph(edges_cnt, nodes_cnt, set(labels))


def build_two_cycle_graph(n: int, m: int, labels: Tuple[str, str], path="./test2.dot"):
    graph = cfpq_data.labeled_two_cycles_graph(n, m, labels=labels)
    pydot_graph = networkx.drawing.nx_pydot.to_pydot(graph)
    pydot_graph.write_raw(path)


def graph_to_nfa(
    graph: MultiDiGraph, start_states: Set[int], final_states: Set[int]
) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton.from_networkx(graph)
    all_states = nfa.states
    if not start_states or not final_states:
        for st in all_states:
            nfa.add_start_state(st)
            nfa.add_final_state(st)
    else:
        for st in start_states:
            nfa.add_start_state(State(st))
        for st in final_states:
            nfa.add_final_state(State(st))
    return nfa
