from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    DeterministicFiniteAutomaton,
    State,
    Symbol,
)
import numpy as np
from numpy.typing import NDArray
from scipy.sparse import csr_array, kron
from typing import Iterable
from networkx import MultiDiGraph
from task2 import regex_to_dfa, graph_to_nfa


class AdjacencyMatrixFA:
    def __init__(
        self,
        fa: (NondeterministicFiniteAutomaton | DeterministicFiniteAutomaton | None),
    ):
        self.states_count: int = 0
        self.start_states = set()
        self.final_states = set()
        self.sparse_matrices: dict[Symbol, csr_array] = {}

        if fa is None:
            return

        isDeterministic = isinstance(fa, DeterministicFiniteAutomaton)

        # get FA transitions
        transitions_dict: dict = fa.to_dict()
        transitions: list[tuple] = list(transitions_dict.items())

        # set nodes
        self.start_states = set(int(x._value) for x in fa.start_states)
        self.final_states = set(int(x._value) for x in fa.final_states)

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
        for key in list(matrices_dict.keys()):
            self.sparse_matrices[key] = csr_array(matrices_dict[key], dtype=np.bool_)

    def accepts(self, word: Iterable[Symbol]) -> bool:
        # list with FA configurations
        confs: list[(int, Iterable[Symbol])] = []

        # add start configurations
        for start_state in self.start_states:
            confs.append((start_state, word))

        while True:
            # if we can't find accept state
            if not confs:
                return False

            cur_conf = confs.pop()

            cur_state = cur_conf[0]
            cur_word = cur_conf[1]

            # accept word
            if (not cur_word) and (cur_state in self.final_states):
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
        adj_matrix: NDArray[np.bool_] = np.zeros(
            shape=(self.states_count, self.states_count), dtype=np.bool_
        )

        for matrix in self.sparse_matrices.values():
            adj_matrix = adj_matrix | matrix.toarray()

        for start_node in self.start_states:
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

        for start_node in self.start_states:
            for final_node in self.final_states:
                if start_node != final_node and matrix[start_node, final_node]:
                    return False  # if FA graph have path from start to finish

        return True


def intersect_automata(
    automaton1: AdjacencyMatrixFA, automaton2: AdjacencyMatrixFA
) -> AdjacencyMatrixFA:
    a1, a2 = automaton1, automaton2

    new_a = AdjacencyMatrixFA(None)
    new_a.states_count = a1.states_count * a2.states_count

    for sym, m1 in a1.sparse_matrices.items():
        if sym in a2.sparse_matrices:
            m2 = a2.sparse_matrices[sym]
            prod: csr_array = kron(m1, m2, format="csr")
            new_a.sparse_matrices[sym] = prod

    # add start/final states
    for s1 in range(a1.states_count):
        for s2 in range(a2.states_count):
            new_index = a2.states_count * s1 + s2

            if (s1 in a1.start_states) and (s2 in a2.start_states):
                new_a.start_states.add(new_index)
            if (s1 in a1.final_states) and (s2 in a2.final_states):
                new_a.final_states.add(new_index)

    return new_a


def tensor_based_rpq(
    graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int], regex: str
) -> list[tuple]:
    nfa = graph_to_nfa(graph, start_nodes, final_nodes)
    dfa = regex_to_dfa(regex)

    print(dfa.states)

    mfa1 = AdjacencyMatrixFA(nfa)
    mfa2 = AdjacencyMatrixFA(dfa)

    new_mfa = intersect_automata(mfa1, mfa2)

    # complementation of languages
    adj_matrix = new_mfa.transitive_сlosure()
    pairs: set[tuple[int, int]] = set()

    for graph_start in start_nodes:
        for graph_final in final_nodes:
            for regex_start in mfa2.start_states:
                for regex_final in mfa2.final_states:
                    start_index = mfa2.states_count * graph_start + regex_start
                    final_index = mfa2.states_count * graph_final + regex_final

                    if adj_matrix[start_index, final_index]:
                        pairs.add((graph_start, graph_final))

    return list(pairs)


fa = NondeterministicFiniteAutomaton()
fa.add_transitions([(0, "a", 1), (1, "c", 2), (1, "a", 0)])

tensor_based_rpq(fa.to_networkx(), set([0]), set([2]), "a*.c")
