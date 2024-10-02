from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    DeterministicFiniteAutomaton,
    State,
    Symbol,
)
import numpy as np
from networkx import MultiDiGraph
from numpy.typing import NDArray
from scipy.sparse import csr_array, kron
from typing import Iterable
from task2 import graph_to_nfa, regex_to_dfa


class AdjacencyMatrixFA:
    def __init__(
        self,
        fa: (NondeterministicFiniteAutomaton | DeterministicFiniteAutomaton | None),
    ):
        self.states_count: int = 0
        self.states: list[State] = []
        self.start_states_is: list[int] = []  # indexes of states
        self.final_states_is: list[int] = []  # indexes of states
        self.sparse_matrices: dict[Symbol, csr_array] = {}

        if fa is None:
            return

        isDeterministic = isinstance(fa, DeterministicFiniteAutomaton)

        # get FA transitions
        transitions_dict: dict = fa.to_dict()
        transitions: list[tuple] = list(transitions_dict.items())

        # set states
        self.states = list(fa.states)
        self.states_count = len(fa.states)

        for i in range(self.states_count):
            state: State = self.states[i]

            if state in fa.start_states:
                self.start_states_is.append(i)
            if state in fa.final_states:
                self.final_states_is.append(i)

        # dictionary for bool decomposition
        matrices_dict: dict[Symbol, NDArray[np.bool_]] = {}

        matrix_shape = (self.states_count, self.states_count)
        # ^ there may be an error, since there may be states that are not in order

        for source_node, dests in transitions:
            # (source_node, {sym: dest_node , ...})
            # index of source_node
            source_node_i: int = self.states.index(source_node)

            for sym, dest in dests.items():
                # DFA: (sym, dest_node)
                # NFA: (sym, {dest_node})
                sym: Symbol = sym._value

                if sym not in matrices_dict:
                    matrices_dict[sym] = np.zeros(shape=matrix_shape, dtype=np.bool_)

                if isDeterministic:
                    dest_node_i: int = self.states.index(dest)

                    matrices_dict[sym][source_node_i, dest_node_i] = True

                else:
                    # different transitions from one state
                    dest_nodes: set[State] = dest

                    for dest_node in dest_nodes:
                        dest_node_i: int = self.states.index(dest_node)
                        matrices_dict[sym][source_node_i, dest_node_i] = True

        # transform to sparse matrices
        for key in list(matrices_dict.keys()):
            self.sparse_matrices[key] = csr_array(matrices_dict[key], dtype=np.bool_)

    def accepts(self, word: Iterable[Symbol]) -> bool:
        # list with FA configurations
        confs: list[(int, list[Symbol])] = []

        # add start configurations
        for start_state_i in self.start_states_is:
            confs.append((start_state_i, list(word)))  # indexes of states + words

        while True:
            # if we can't find accept state
            if not confs:
                return False

            cur_conf = confs.pop()

            cur_state_i = cur_conf[0]
            cur_word = cur_conf[1]

            # accept word
            if (not cur_word) and (cur_state_i in self.final_states_is):
                return True

            cur_sym = cur_word[0]

            if cur_sym not in self.sparse_matrices:
                # can't find matrix for this symbol
                continue
            else:
                matrix = self.sparse_matrices[cur_sym]

                # add new confs (by matrix row)
                row_states_is = range(matrix.shape[0])
                next_states_is = [
                    next_state_i
                    for next_state_i in row_states_is
                    if matrix[cur_state_i, next_state_i]
                ]

                for next_state_i in next_states_is:
                    confs.append((next_state_i, cur_word[1:]))

    def transitive_сlosure(self) -> NDArray[np.bool_]:
        adj_matrix: NDArray[np.bool_] = np.zeros(
            shape=(self.states_count, self.states_count), dtype=np.bool_
        )

        for matrix in self.sparse_matrices.values():
            adj_matrix = adj_matrix | matrix.toarray()

        for start_node in self.start_states_is:
            adj_matrix[start_node, start_node] = True

        for k in range(self.states_count):
            for i in range(self.states_count):
                for j in range(self.states_count):
                    adj_matrix[i][j] = adj_matrix[i][j] or (
                        adj_matrix[i][k] and adj_matrix[k][j]
                    )

        return adj_matrix

    def is_empty(self) -> bool:
        matrix: NDArray[np.bool_] = self.transitive_сlosure()

        for start_node in self.start_states_is:
            for final_node in self.final_states_is:
                if matrix[start_node, final_node]:
                    return False  # if FA graph have path from start to finish

        return True


def intersect_automata(
    automaton1: AdjacencyMatrixFA, automaton2: AdjacencyMatrixFA
) -> AdjacencyMatrixFA:
    a1, a2 = automaton1, automaton2

    new_a = AdjacencyMatrixFA(None)
    new_a.states_count = a1.states_count * a2.states_count

    # kron prod
    for sym, m1 in a1.sparse_matrices.items():
        if sym in a2.sparse_matrices:
            m2 = a2.sparse_matrices[sym]
            prod: csr_array = kron(m1, m2, format="csr")
            new_a.sparse_matrices[sym] = prod

    # add start/final states
    for s1 in range(a1.states_count):
        for s2 in range(a2.states_count):
            new_index = a2.states_count * s1 + s2
            new_state = (a1.states[s1], a2.states[s2])

            new_a.states.append(State(new_state))

            if (s1 in a1.start_states_is) and (s2 in a2.start_states_is):
                new_a.start_states_is.append(new_index)
            if (s1 in a1.final_states_is) and (s2 in a2.final_states_is):
                new_a.final_states_is.append(new_index)

    return new_a


def tensor_based_rpq(
    graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int], regex: str
) -> list[tuple]:
    nfa = graph_to_nfa(graph, start_nodes, final_nodes)
    dfa = regex_to_dfa(regex)

    mfa1 = AdjacencyMatrixFA(nfa)
    mfa2 = AdjacencyMatrixFA(dfa)

    new_mfa = intersect_automata(mfa1, mfa2)

    # complementation of languages
    adj_matrix = new_mfa.transitive_сlosure()

    pairs: set[tuple[int, int]] = set()

    # [!] start_nodes & final_nodes not indexes
    for graph_start in start_nodes:
        for graph_final in final_nodes:
            for regex_start_i in mfa2.start_states_is:
                for regex_final_i in mfa2.final_states_is:
                    graph_start_i = mfa1.states.index(graph_start)
                    graph_final_i = mfa1.states.index(graph_final)

                    start_index = mfa2.states_count * graph_start_i + regex_start_i
                    final_index = mfa2.states_count * graph_final_i + regex_final_i

                    if adj_matrix[start_index, final_index]:
                        pairs.add((graph_start, graph_final))

    return list(pairs)
