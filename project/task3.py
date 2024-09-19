from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    DeterministicFiniteAutomaton,
    State,
    Symbol,
)
import numpy as np
from numpy.typing import NDArray
from scipy.sparse import csr_array
from typing import Iterable


class AdjacencyMatrixFA:
    def __init__(
        self, fa: (NondeterministicFiniteAutomaton | DeterministicFiniteAutomaton)
    ):
        isDeterministic = isinstance(fa, DeterministicFiniteAutomaton)

        # get FA transitions
        transitions_dict = fa.to_dict()
        transitions: list[tuple] = list(transitions_dict.items())

        # set start / final nodes
        self.start_nodes: set[int] = set(int(x._value) for x in fa.start_states)
        self.final_nodes: set[int] = set(int(x._value) for x in fa.final_states)

        # dictionary for bool decomposition
        matrices_dict: dict[Symbol, NDArray[np.bool_]] = {}

        self.states_count = len(fa.states)
        matrix_shape = (self.states_count, self.states_count)
        # ^ there may be an error, since there may be states that are not in order

        for source_node, dests in transitions:
            # (source_node, {sym: dest_node , ...})
            source_node: int = int(source_node._value)

            for sym, dest in dests.items():
                # DFA: (sym, dest_node)
                # NFA: (sym, {dest_node})
                sym: Symbol = sym._value

                if sym not in matrices_dict:
                    matrices_dict[sym] = np.zeros(shape=matrix_shape, dtype=np.bool_)

                if isDeterministic:
                    dest_node: int = dest._value

                    matrices_dict[sym][source_node, dest_node] = True

                else:
                    dest_nodes: dict[int] = dest

                    for dest_node in dest_nodes:
                        dest_node = dest_node._value
                        matrices_dict[sym][source_node, dest_node] = True

        # transform to sparse matrices
        self.sparse_matrices: dict[Symbol, csr_array] = {}

        for key in list(matrices_dict.keys()):
            self.sparse_matrices[key] = csr_array(matrices_dict[key], dtype=np.bool_)

    def accepts(self, word: Iterable[Symbol]) -> bool:
        # list with FA configurations
        confs: list[(int, Iterable[Symbol])] = []

        # add start configurations
        for start_state in self.start_nodes:
            confs.append((start_state, word))

        while True:
            # if we can't find accept state
            if not confs:
                return False

            cur_conf = confs.pop()

            cur_state = cur_conf[0]
            cur_word = cur_conf[1]

            # accept word
            if (not cur_word) and (cur_state in self.final_nodes):
                return True

            cur_sym = cur_word[0]

            if cur_sym not in self.sparse_matrices:
                # can't find matrix for this symbol
                continue
            else:
                matrix = self.sparse_matrices[cur_sym]

                # add new confs (by matrix row)
                row_states = range(matrix.shape[0])
                next_states = [
                    next_state
                    for next_state in row_states
                    if matrix[cur_state, next_state]
                ]

                for next_state in next_states:
                    confs.append((next_state, cur_word[1:]))

    def transitive_сlosure(self) -> NDArray[np.bool_]:
        # get adjacency matrix from bool decomposition
        bool_matrices: list[csr_array] = list(self.sparse_matrices.values())

        adj_matrix: NDArray[np.bool_] = np.zeros(
            shape=(self.states_count, self.states_count), dtype=np.bool_
        )

        for matrix in self.sparse_matrices.values():
            adj_matrix = adj_matrix | matrix.toarray()

        for k in range(self.states_count):
            for i in range(self.states_count):
                for j in range(self.states_count):
                    adj_matrix[i][j] = adj_matrix[i][j] or (
                        adj_matrix[i][k] and adj_matrix[k][j]
                    )

        return adj_matrix

    def is_empty(self) -> bool:
        matrix: NDArray[np.bool_] = self.transitive_сlosure()

        for start_node in self.start_nodes:
            for final_node in self.final_nodes:
                if start_node != final_node and matrix[start_node, final_node]:
                    return False  # if FA graph have path from start to finish

        return True


fa = NondeterministicFiniteAutomaton()
fa.add_transitions([(0, "a", 1), (0, "b", 2), (1, "c", 2), (1, "a", 0)])
fa.add_start_state(2)
fa.add_final_state(2)

amf = AdjacencyMatrixFA(fa)
