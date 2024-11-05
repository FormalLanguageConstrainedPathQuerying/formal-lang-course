import networkx as nx
import numpy as np
import pyformlang
import pyformlang.cfg
from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
)
import pyformlang.rsa
from scipy.sparse import csr_matrix

from project.task2 import graph_to_nfa
from project.task3 import AdjacencyMatrixFA, intersect_automata


def tensor_based_cfpq(
    rsa: pyformlang.rsa.RecursiveAutomaton,
    graph: nx.DiGraph,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
) -> set[tuple[int, int]]:
    nfa_of_rsm = NondeterministicFiniteAutomaton()

    def concat_nont(nont, s):
        return nont, s

    for nont, box in rsa.boxes.items():
        dfa = box.dfa

        for s in dfa.final_states | dfa.start_states:
            if s in dfa.final_states:
                nfa_of_rsm.add_final_state(concat_nont(nont, s))
            if s in dfa.start_states:
                nfa_of_rsm.add_start_state(concat_nont(nont, s))

        for u, v, label in dfa.to_networkx().edges(data="label"):
            nfa_of_rsm.add_transition(concat_nont(nont, u), label, concat_nont(nont, v))

    adj_rsa = AdjacencyMatrixFA(nfa_of_rsm)
    adj_graph = AdjacencyMatrixFA(graph_to_nfa(graph, start_nodes, final_nodes))

    for nont in rsa.boxes:
        for adj in (adj_graph, adj_rsa):
            if nont not in adj.adjacency_matrixes_boolean_decomposition:
                adj.adjacency_matrixes_boolean_decomposition[nont] = csr_matrix(
                    (adj.state_count, adj.state_count), dtype=np.bool_
                )

    prev_nonzero_count = 0
    new_nonzero_count = None

    while prev_nonzero_count != new_nonzero_count:
        prev_nonzero_count = new_nonzero_count
        intersection = intersect_automata(adj_rsa, adj_graph)
        transitive_closure = intersection.transitive_closure()
        for row, column in zip(*transitive_closure.nonzero()):
            row_state = intersection.state_of_indexes[row]
            column_state = intersection.state_of_indexes[column]
            try:
                (row_symbol, row_rsm_state), row_graph_state = row_state
                (column_symbol, column_rsm_state), column_graph_state = column_state
            except ValueError:
                continue
            if (
                row_symbol == column_symbol
                and row_rsm_state in rsa.boxes[row_symbol].dfa.start_states
                and column_rsm_state in rsa.boxes[row_symbol].dfa.final_states
            ):
                row_graph_index = adj_graph.index_of_states[row_graph_state]
                column_graph_index = adj_graph.index_of_states[column_graph_state]

                adj_graph.adjacency_matrixes_boolean_decomposition[row_symbol][
                    row_graph_index, column_graph_index
                ] = True

        new_nonzero_count = sum(
            adj_graph.adjacency_matrixes_boolean_decomposition[
                nonterminal
            ].count_nonzero()
            for nonterminal in adj_graph.adjacency_matrixes_boolean_decomposition
        )

    res = set()
    for n in adj_graph.start_states:
        for m in adj_graph.final_states:
            if adj_graph.adjacency_matrixes_boolean_decomposition[rsa.initial_label][
                adj_graph.index_of_states[n], adj_graph.index_of_states[m]
            ]:
                res.add((n, m))
    return res


def cfg_to_rsm(cfg: pyformlang.cfg.CFG) -> pyformlang.rsa.RecursiveAutomaton:
    return ebnf_to_rsm(cfg.to_text())


def ebnf_to_rsm(ebnf: str) -> pyformlang.rsa.RecursiveAutomaton:
    return pyformlang.rsa.RecursiveAutomaton.from_text(ebnf)
