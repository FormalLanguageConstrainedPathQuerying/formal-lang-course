from itertools import product
import networkx as nx
import scipy.sparse as sp
from pyformlang import rsa, cfg as pycfg
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State
from scipy.sparse import csc_array
from project.task2 import graph_to_nfa
from project.task3 import AdjacencyMatrixFA, intersect_automata
from typing import Set, Tuple


def cfg_to_rsm(cfg: pycfg.CFG) -> rsa.RecursiveAutomaton:
    return rsa.RecursiveAutomaton.from_text(cfg.to_text())


def ebnf_to_rsm(ebnf: str) -> rsa.RecursiveAutomaton:
    return rsa.RecursiveAutomaton.from_text(ebnf)


def tensor_based_cfpq(
    rsm: rsa.RecursiveAutomaton,
    graph: nx.DiGraph,
    start_nodes: Set[int] | None = None,
    final_nodes: Set[int] | None = None,
    matrix_type=sp.csr_matrix,
) -> Set[Tuple[int, int]]:
    nfa = NondeterministicFiniteAutomaton()
    for nonterminal, box in rsm.boxes.items():
        dfa = box.dfa
        for state in dfa.start_states:
            nfa.add_start_state(State((nonterminal, state)))
        for state in dfa.final_states:
            nfa.add_final_state(State((nonterminal, state)))
        for src, dst, label in dfa.to_networkx().edges(data="label"):
            nfa.add_transition(
                State((nonterminal, src)), label, State((nonterminal, dst))
            )

    bool_rsm = AdjacencyMatrixFA(nfa)
    bool_graph = AdjacencyMatrixFA(
        graph_to_nfa(graph, start_nodes, final_nodes), matrix_type=matrix_type
    )

    for nonterminal in rsm.boxes:
        if nonterminal not in bool_rsm.symbol_matrices:
            bool_rsm.symbol_matrices[nonterminal] = csc_array(
                (bool_rsm.states_number, bool_rsm.states_number), dtype=bool
            )
        if nonterminal not in bool_graph.symbol_matrices:
            bool_graph.symbol_matrices[nonterminal] = csc_array(
                (bool_graph.states_number, bool_graph.states_number), dtype=bool
            )

    prev_nonzero, curr_nonzero = -1, 0
    while prev_nonzero != curr_nonzero:
        prev_nonzero = curr_nonzero
        intersection = intersect_automata(bool_rsm, bool_graph)
        closure = intersection.transitive_closure()
        for src, dst in zip(*closure.nonzero()):
            row_state, col_state = (
                intersection.int_to_states[src],
                intersection.int_to_states[dst],
            )
            row_inner, row_graph_state = row_state.value
            row_label, row_rsm_state = row_inner.value
            col_inner, col_graph_state = col_state.value
            col_label, col_rsm_state = col_inner.value
            if (
                row_label == col_label
                and row_rsm_state in rsm.boxes[row_label].dfa.start_states
                and col_rsm_state in rsm.boxes[row_label].dfa.final_states
            ):
                start_idx = bool_graph.states_to_int[row_graph_state]
                finish_idx = bool_graph.states_to_int[col_graph_state]
                bool_graph.symbol_matrices[row_label][start_idx, finish_idx] = True
        curr_nonzero = sum(mat.nnz for mat in bool_graph.symbol_matrices.values())

    return {
        (bool_graph.int_to_states[start], bool_graph.int_to_states[finish])
        for start, finish in product(bool_graph.start_states, bool_graph.final_states)
        if bool_graph.symbol_matrices[rsm.initial_label][start, finish]
    }
