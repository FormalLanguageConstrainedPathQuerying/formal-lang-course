from typing import Optional

from networkx import DiGraph, MultiDiGraph
from pyformlang.cfg import CFG
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State, Symbol
from pyformlang.rsa import RecursiveAutomaton
from scipy.sparse import csc_matrix

from project.adjacency_matrix import AdjacencyMatrixFA, intersect_automata
from project.finite_automaton import graph_to_nfa


def rsm_to_nfa(rsm: RecursiveAutomaton) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton()

    for nonterm, box in rsm.boxes.items():
        dfa = box.dfa

        for st in dfa.start_states:
            nfa.add_start_state(State((nonterm, st.value)))
        for st in dfa.final_states:
            nfa.add_final_state(State((nonterm, st.value)))

        transitions = dfa.to_networkx().edges(data="label")
        for u, v, label in transitions:
            start = State((nonterm, u))
            end = State((nonterm, v))
            nfa.add_transition(start, label, end)

    return nfa


def tensor_based_cfpq(
    rsm: RecursiveAutomaton,
    graph: DiGraph,
    start_nodes: Optional[set[int]] = None,
    final_nodes: Optional[set[int]] = None,
) -> set[tuple[int, int]]:
    start_nodes = start_nodes or set(graph.nodes)
    final_nodes = final_nodes or set(graph.nodes)
    rsm_m = AdjacencyMatrixFA(rsm_to_nfa(rsm))
    graph_m = AdjacencyMatrixFA(
        graph_to_nfa(MultiDiGraph(graph), start_nodes, final_nodes)
    )

    while True:
        closure = intersect_automata(graph_m, rsm_m).transitive_closure()
        delta: dict[Symbol, csc_matrix] = {}
        for i, j in zip(*closure.nonzero()):
            rsm_i, rsm_j = i % rsm_m.states_count, j % rsm_m.states_count
            if rsm_i in rsm_m.start_states and rsm_j in rsm_m.final_states:
                nonterm = rsm_m.indices_states[rsm_i].value[0]

                graph_i, graph_j = i // rsm_m.states_count, j // rsm_m.states_count
                if (
                    nonterm in graph_m.matrices
                    and graph_m.matrices[nonterm][graph_i, graph_j]
                ):
                    continue

                delta[nonterm] = delta.get(
                    nonterm,
                    csc_matrix(
                        (graph_m.states_count, graph_m.states_count), dtype=bool
                    ),
                )
                delta[nonterm][graph_i, graph_j] = True
        if not delta:
            break
        for symbol in delta:
            if symbol not in graph_m.matrices:
                graph_m.matrices[symbol] = delta[symbol]
            else:
                graph_m.matrices[symbol] += delta[symbol]

    start_m = graph_m.matrices.get(rsm.initial_label)
    if start_m is None:
        return set()

    return {
        (start, final)
        for start in start_nodes
        for final in final_nodes
        if start_m[graph_m.states[State(start)], graph_m.states[State(final)]]
    }


def cfg_to_rsm(cfg: CFG) -> RecursiveAutomaton:
    return RecursiveAutomaton.from_text(cfg.to_text())


def ebnf_to_rsm(ebnf: str) -> RecursiveAutomaton:
    return RecursiveAutomaton.from_text(ebnf)
