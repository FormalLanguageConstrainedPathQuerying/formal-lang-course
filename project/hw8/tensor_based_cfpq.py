import itertools
from typing import Dict

import pyformlang
from pyformlang.finite_automaton import Symbol, State
import networkx as nx
from project.tools.rsm_tools import (
    rsm_to_nfa,
)
from project.hw3.AdjacencyMatrixFA import AdjacencyMatrixFA, intersect_automata
from project.hw2.graph_to_nfa_tool import graph_to_nfa
from scipy import sparse


def tensor_based_cfpq(
    rsm: pyformlang.rsa.RecursiveAutomaton,
    graph: nx.DiGraph,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
) -> set[tuple[int, int]]:
    rsm_fa = rsm_to_nfa(rsm)
    rsm_adj = AdjacencyMatrixFA(rsm_fa)

    graph = nx.MultiDiGraph(graph)
    graph_fa = graph_to_nfa(graph, start_nodes, final_nodes)
    graph_adj = AdjacencyMatrixFA(graph_fa)

    def delta(
        tc: sparse.csr_matrix, intersection_: AdjacencyMatrixFA
    ) -> Dict[Symbol, sparse.csr_matrix]:
        res: dict[Symbol, sparse.csr_matrix] = {}

        for ind_from, ind_to in zip(*tc.nonzero()):
            kron_state_start_st, kron_state_fin_st = intersection_.get_state_by_idx(
                [ind_from, ind_to]
            )
            gr_start_st, rsm_start_st = (
                State(kron_state_start_st.value[0]),
                State(kron_state_start_st.value[1]),
            )
            gr_fin_st, rsm_fin_st = (
                State(kron_state_fin_st.value[0]),
                State(kron_state_fin_st.value[1]),
            )

            gr_start_ind, gr_fin_ind = graph_adj.get_idx_by_state(
                [gr_start_st, gr_fin_st]
            )
            assert rsm_start_st.value[0] == rsm_fin_st.value[0]
            if not (
                (rsm_start_st in rsm_adj.start_states)
                and (rsm_fin_st in rsm_adj.final_states)
            ):
                continue

            label = rsm_start_st.value[0]
            size = graph_adj.states_cnt
            if (
                label not in graph_adj.boolean_decomposition
                or not graph_adj.boolean_decomposition[label][gr_start_ind, gr_fin_ind]
            ):
                res.setdefault(label, sparse.csr_matrix((size, size), dtype=bool))[
                    gr_start_ind, gr_fin_ind
                ] = True
        return res

    while True:
        intersection_automatas = intersect_automata(graph_adj, rsm_adj)
        tc = intersection_automatas.transitive_closure()
        delta_ = delta(tc, intersection_automatas)

        if not delta_:
            break
        for lab, matr in delta_.items():
            if lab in graph_adj.boolean_decomposition:
                graph_adj.boolean_decomposition[lab] += matr
            else:
                graph_adj.boolean_decomposition[lab] = matr

    start_symb = rsm.initial_label
    if start_symb in graph_adj.boolean_decomposition:
        start_m = graph_adj.boolean_decomposition[start_symb]
        return {
            (start, final)
            for (start, final) in itertools.product(start_nodes, final_nodes)
            if start_m[
                graph_adj.labeled_node_numbers[State(start)],
                graph_adj.labeled_node_numbers[State(final)],
            ]
        }
    return set()
