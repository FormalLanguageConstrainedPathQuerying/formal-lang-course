import itertools
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
    boolean_decomposition: dict[Symbol, sparse.csr_matrix]
    start_states_ind: set[int]
    final_states_ind: set[int]
    start_states: set[State]
    final_states: set[State]

    def get_idx_by_state(self, states: list[State]) -> list[int]:
        return list(map(lambda x: self.labeled_node_numbers[x], states))

    def get_state_by_idx(self, ids: list[int]) -> list[State]:
        return list(map(lambda x: self.numbered_node_labels[x], ids))

    def __init__(self, fa: NondeterministicFiniteAutomaton = None):
        self.boolean_decomposition = {}
        self.start_states_ind = set()
        self.final_states_ind = set()
        self.labeled_node_numbers = {}
        self.numbered_node_labels = {}
        self.start_states = set()
        self.final_states = set()

        if fa is None:
            self.states_cnt = 0
            return

        self.states_cnt = len(fa.states)

        for ind, state in enumerate(fa.states, 0):
            self.labeled_node_numbers[state] = ind
            self.numbered_node_labels[ind] = state

        for start_state in fa.start_states:
            self.start_states_ind.add(self.labeled_node_numbers[start_state])
            self.start_states.add(start_state)

        for final_state in fa.final_states:
            self.final_states_ind.add(self.labeled_node_numbers[final_state])
            self.final_states.add(final_state)

        graph = fa.to_networkx()
        edges = graph.edges(data="label")

        nodes_connectivity = {}
        labels = set()

        for edge in edges:
            u = edge[0]
            v = edge[1]
            label = edge[2]
            # assert isinstance(label, Symbol)
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

    # def get_state_to_idx(self, states: list[State]) -> list[int]:
    #     return list(map(lambda x: self.labeled_node_numbers[x], states))

    def get_start_and_final(self) -> list[tuple[State, State]]:
        transition_matrix = self.transitive_closure()
        start_ids = self.get_idx_by_state(list(self.start_states))
        final_ids = self.get_idx_by_state(list(self.final_states))
        return [
            (self.numbered_node_labels[start], self.numbered_node_labels[final])
            for start in start_ids
            for final in final_ids
            if transition_matrix[start, final]
        ]

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

    new_states = [State((automaton1.numbered_node_labels[ind1], automaton2.numbered_node_labels[ind2]))
                  for ind1 in range(fa1_dim) for ind2 in range(fa2_dim)]

    new_ind_to_state = {state: ind for (state, ind) in enumerate(new_states)}
    new_state_to_ind = {ind: state for (state, ind) in enumerate(new_states)}
    kron_labels = (
        automaton1.boolean_decomposition.keys() & automaton2.boolean_decomposition.keys()
    )

    inter_boolean_decomposition_matrices = {}

    for label in kron_labels:
        inter_boolean_decomposition_matrices[label] = sparse.kron(
            automaton1.boolean_decomposition[label],
            automaton2.boolean_decomposition[label],
        )
    new_start_states = set(itertools.product(map(lambda x: x.value, automaton1.start_states),
                                             map(lambda x: x.value, automaton2.start_states)))
    new_start_states_ind = set(map(lambda state: new_state_to_ind[state], new_start_states))

    new_final_states = set(itertools.product(map(lambda x: x.value, automaton1.final_states),
                                             map(lambda x: x.value, automaton2.final_states)))
    new_final_states_ind = set(map(lambda state: new_state_to_ind[state], new_final_states))

    for symb in kron_labels:
        inter_boolean_decomposition_matrices[symb] = sparse.kron(automaton1.boolean_decomposition[symb],
                                                                 automaton2.boolean_decomposition[symb]).tocsr()
    adjacency_matrix_fa = AdjacencyMatrixFA()
    adjacency_matrix_fa.states_cnt = fa1_dim * fa2_dim
    adjacency_matrix_fa.boolean_decomposition = inter_boolean_decomposition_matrices
    adjacency_matrix_fa.start_states = new_start_states
    adjacency_matrix_fa.final_states = new_final_states

    adjacency_matrix_fa.start_states_ind = new_start_states_ind
    adjacency_matrix_fa.final_states_ind = new_final_states_ind
    adjacency_matrix_fa.labeled_node_numbers = new_state_to_ind
    adjacency_matrix_fa.numbered_node_labels = new_ind_to_state
    return adjacency_matrix_fa


def tensor_based_rpq(
    regex: str, graph: nx.MultiDiGraph, start_nodes: set[int], final_nodes: set[int]
) -> set[tuple[int, int]]:
    regex_dfa = regex_to_dfa(regex)
    regex_adjacency_matrix_fa = AdjacencyMatrixFA(regex_dfa)

    graph_nfa = graph_to_nfa(graph, start_nodes, final_nodes)
    graph_adjacency_matrix_fa = AdjacencyMatrixFA(graph_nfa)

    intersect = intersect_automata(graph_adjacency_matrix_fa, regex_adjacency_matrix_fa)

    rpq_answer = tuple(zip(*intersect.get_start_and_final()))
    rpq_start_states, rpq_final_states = ([], []) if not rpq_answer else rpq_answer

    rpq_start_state_values = list(map(lambda x: x.value[0], rpq_start_states))
    rpq_final_state_values = list(map(lambda x: x.value[0], rpq_final_states))
    return set(zip(rpq_start_state_values, rpq_final_state_values))
