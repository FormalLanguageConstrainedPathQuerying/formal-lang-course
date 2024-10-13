from typing import Iterable
from pyformlang.finite_automaton import Symbol, State
import numpy as np
from typing import Any
from scipy import sparse
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from project.hw2.graph_to_nfa_tool import graph_to_nfa
from project.hw2.regex_to_dfa_tool import regex_to_dfa
from project.tools.vector_tool import create_bool_vector
import networkx as nx


class AdjacencyMatrixFA:
    states_cnt: int
    # adjacent_vertices: dict  # stores pairs of nodes that connected by an edge
    labeled_node_numbers: dict[
        State, int
    ]  # stores key: value structure, key - node label, value - node index
    numbered_node_labels: dict[int, State]
    boolean_decomposition: dict[Any, sparse.csr_matrix]
    start_states_ind: set[int]
    final_states_ind: set[int]

    def get_states_by_indexes(self, ind_list: list[id]) -> list[State]:
        return list(map(lambda ind: self.numbered_node_labels[ind], ind_list))

    def __init__(self, fa: NondeterministicFiniteAutomaton = None):
        self.boolean_decomposition = {}
        self.start_states_ind = set()
        self.final_states_ind = set()
        self.labeled_node_numbers = {}
        self.numbered_node_labels = {}

        if fa is None:
            self.states_cnt = 0
            return

        self.states_cnt = len(fa.states)

        for ind, state in enumerate(fa.states, 0):
            self.labeled_node_numbers[state] = ind
            self.numbered_node_labels[ind] = state

        for start_state in fa.start_states:
            self.start_states_ind.add(self.labeled_node_numbers[start_state])

        for final_state in fa.final_states:
            self.final_states_ind.add(self.labeled_node_numbers[final_state])

        graph = fa.to_networkx()
        edges = graph.edges(data="label")

        nodes_connectivity = {}
        labels = set()

        for edge in edges:
            u = edge[0]
            v = edge[1]
            label = edge[2]

            if label is not None:
                nodes_connectivity.setdefault(label, []).append((u, v))
                labels.add(label)

        for label in labels:
            data = np.ones(len(nodes_connectivity[label]), dtype=bool)
            rows = list(
                map(
                    lambda conn: self.labeled_node_numbers[conn[0]],
                    nodes_connectivity[label],
                )
            )
            columns = list(
                map(
                    lambda conn: self.labeled_node_numbers[conn[1]],
                    nodes_connectivity[label],
                )
            )

            decomposed_matrix = sparse.csr_matrix(
                (data, (rows, columns)),
                shape=(self.states_cnt, self.states_cnt),
            )

            self.boolean_decomposition[label] = decomposed_matrix

    def transitive_closure(self):
        transitive_closure = sparse.csr_matrix(
            (
                np.ones(self.states_cnt, dtype=bool),
                (range(self.states_cnt), range(self.states_cnt)),
            ),
            shape=(self.states_cnt, self.states_cnt),
        )

        for matrix in self.boolean_decomposition.values():
            transitive_closure = matrix + transitive_closure

        transitive_closure_matrix = transitive_closure ** (self.states_cnt - 1)

        return transitive_closure_matrix.tocsr()

    def accepts(self, word: Iterable[Symbol]) -> bool:
        states_ind_vector = create_bool_vector(self.states_cnt, self.start_states_ind)

        for symbol in word:
            states_ind_vector = states_ind_vector @ self.boolean_decomposition[symbol]

        final_states_ind_vector = create_bool_vector(
            self.states_cnt, self.final_states_ind
        )

        return np.any(states_ind_vector & final_states_ind_vector)

    def is_empty(self) -> bool:
        states_ones = create_bool_vector(self.states_cnt, self.start_states_ind)

        transitive_closure_matrix = self.transitive_closure()

        states_ind_vector = states_ones @ transitive_closure_matrix

        final_states_ind_vector = create_bool_vector(
            self.states_cnt, self.final_states_ind
        )

        return not np.any(states_ind_vector & final_states_ind_vector)


def intersect_automata(
    automaton1: AdjacencyMatrixFA, automaton2: AdjacencyMatrixFA
) -> AdjacencyMatrixFA:
    fa1_dim = automaton1.states_cnt
    fa2_dim = automaton2.states_cnt
    kron_matrix_size = fa1_dim * fa2_dim

    inter_boolean_decomposition_matrices = {}

    kron_labels = (
        automaton1.boolean_decomposition.keys()
        & automaton2.boolean_decomposition.keys()
    )

    for label in kron_labels:
        inter_boolean_decomposition_matrices[label] = sparse.kron(
            automaton1.boolean_decomposition[label],
            automaton2.boolean_decomposition[label],
        )

    start_states_ind = set()
    final_states_ind = set()

    for start_state_1 in automaton1.start_states_ind:
        for start_state_2 in automaton2.start_states_ind:
            start_states_ind.add(start_state_1 * fa2_dim + start_state_2)

    for final_state_ind1 in automaton1.final_states_ind:
        for final_state_ind2 in automaton2.final_states_ind:
            final_states_ind.add(final_state_ind1 * fa2_dim + final_state_ind2)

    state_to_ind = {}
    ind_to_state = {}

    for i in range(0, kron_matrix_size):
        state_to_ind[i] = i
        ind_to_state[i] = i

    adjacency_matrix_fa = AdjacencyMatrixFA()

    adjacency_matrix_fa.states_cnt = kron_matrix_size
    adjacency_matrix_fa.boolean_decomposition = inter_boolean_decomposition_matrices
    adjacency_matrix_fa.start_states_ind = start_states_ind
    adjacency_matrix_fa.final_states_ind = final_states_ind
    adjacency_matrix_fa.labeled_node_numbers = state_to_ind
    adjacency_matrix_fa.numbered_node_labels = ind_to_state

    return adjacency_matrix_fa


def tensor_based_rpq(
    regex: str, graph: nx.MultiDiGraph, start_nodes: set[int], final_nodes: set[int]
) -> set[tuple[int, int]]:
    regex_dfa = regex_to_dfa(regex)
    regex_adjacency_matrix_fa = AdjacencyMatrixFA(regex_dfa)

    graph_nfa = graph_to_nfa(graph, start_nodes, final_nodes)
    graph_adjacency_matrix_fa = AdjacencyMatrixFA(graph_nfa)

    intersect = intersect_automata(graph_adjacency_matrix_fa, regex_adjacency_matrix_fa)

    transitive_closure_matrix = intersect.transitive_closure()

    res = set()
    for graph_start_state_ind in graph_adjacency_matrix_fa.start_states_ind:
        for regex_start_state_ind in regex_adjacency_matrix_fa.start_states_ind:
            for graph_final_state_ind in graph_adjacency_matrix_fa.final_states_ind:
                for regex_final_state_ind in regex_adjacency_matrix_fa.final_states_ind:
                    intersect_start_state_ind = (
                        graph_start_state_ind * regex_adjacency_matrix_fa.states_cnt
                        + regex_start_state_ind
                    )
                    intersect_final_state_ind = (
                        graph_final_state_ind * regex_adjacency_matrix_fa.states_cnt
                        + regex_final_state_ind
                    )

                    if transitive_closure_matrix[
                        intersect_start_state_ind, intersect_final_state_ind
                    ]:
                        res_start_state = (
                            graph_adjacency_matrix_fa.numbered_node_labels[
                                graph_start_state_ind
                            ]
                        )
                        res_final_state = (
                            graph_adjacency_matrix_fa.numbered_node_labels[
                                graph_final_state_ind
                            ]
                        )

                        res.add((res_start_state, res_final_state))

    return res
