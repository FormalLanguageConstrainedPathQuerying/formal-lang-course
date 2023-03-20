from typing import Set

from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State
from scipy import sparse
from scipy.sparse._compressed import _cs_matrix


class AdjacencyMatrix:
    """
    Class representing Adjacency Matrix
    """
    def __init__(self, nfa: NondeterministicFiniteAutomaton = None):
        if nfa is None:
            self.state_indices = dict()
            self.start_states = set()
            self.final_states = set()
            self.matrix = dict()
        else:
            self.state_indices = {state: index for index, state in enumerate(nfa.states)}
            self.start_states = nfa.start_states
            self.final_states = nfa.final_states
            self.matrix = self.create_matrix(nfa)

    def get_states_len(self):
        """
        :return: number of NFA states
        """
        return len(self.state_indices.keys())

    def get_states(self):
        """
        :return: NFA states
        """
        return self.state_indices.keys()

    def get_start_states_len(self):
        """
        :return: number of  NFA start states
        """
        return len(self.start_states)

    def get_final_states_len(self):
        """
        :return: number of NFA final states
        """
        return len(self.final_states)

    def create_matrix(self, nfa: NondeterministicFiniteAutomaton) -> dict:
        """
        Creates transitive closure dictionary and saves it to internal state
        :param nfa: NFA
        :return: transitive closure dictionary
        """
        matrix = dict()
        nfa_dictionary = nfa.to_dict()
        states_length = self.get_states_len()

        for state_from, transition in nfa_dictionary.items():
            for label, states_to in transition.items():
                if not isinstance(states_to, set):
                    states_to = {states_to}

                for state_to in states_to:
                    index_from = self.state_indices[state_from]
                    index_to = self.state_indices[state_to]
                    if label not in matrix:
                        matrix[label] = sparse.csr_matrix((states_length, states_length), dtype=bool)
                    matrix[label][index_from, index_to] = True
        return matrix

    def get_transitive_closure(self) -> _cs_matrix:
        """
        :return: Transitive closure. Return type is the most generic scipy type for sparce matrices
        """
        result = sum(self.matrix.values())
        curr_nnz = 0
        prev_nnz = result.nnz

        while prev_nnz != curr_nnz:
            result += result.__matmul__(result)
            prev_nnz = curr_nnz
            curr_nnz = result.nnz

        return result

    def index_by_state(self, state):
        return self.state_indices[state]

    def state_by_index(self, index):
        for state, ind in self.state_indices.items():
            if ind == index:
                return state


def intersect_adjacency_matrices(first: AdjacencyMatrix, second: AdjacencyMatrix) -> AdjacencyMatrix:
    """
    Calculates multiplication of two adjacency matrices
    :return: Intersected Adjacency Matrix
    """
    result = AdjacencyMatrix()
    common_symbols = first.matrix.keys().__and__(second.matrix.keys())

    for symbol in common_symbols:
        result.matrix[symbol] = sparse.kron(first.matrix[symbol], second.matrix[symbol], format="csr")

    for state_first, state_first_index in first.state_indices.items():
        for state_second, state_second_index in second.state_indices.items():
            new_state_index = state_first_index * second.get_states_len() + state_second_index
            new_state = new_state_index
            result.state_indices[new_state] = new_state_index

            if state_first in first.start_states and state_second in second.start_states:
                result.start_states.add(new_state)

            if state_first in first.final_states and state_second in second.final_states:
                result.final_states.add(new_state)
    return result


def adjacency_matrix_to_nfa(am: AdjacencyMatrix) -> NondeterministicFiniteAutomaton:
    """
    :param am: Adjacency matrix
    :return: NFA representing am
    """
    nfa = NondeterministicFiniteAutomaton()
    for label, bool_matrix in am.matrix.items():
        for state_from, state_to in zip(*bool_matrix.nonzero()):
            nfa.add_transition(state_from, label, state_to)

    for state in am.start_states:
        nfa.add_start_state(State(state))

    for state in am.final_states:
        nfa.add_final_state(State(state))

    return nfa


def _get_front(first_matrix: AdjacencyMatrix, second_matrix: AdjacencyMatrix, start_state_indices) -> _cs_matrix:
    """
    Helper function to get front row matrx
    """
    front_row_matrix = sparse.dok_matrix((1, first_matrix.get_states_len()), dtype=bool)

    for i in start_state_indices:
        front_row_matrix[0, i] = True
    front_row_matrix = front_row_matrix.tocsr()

    front = sparse.csr_matrix((second_matrix.get_states_len(), first_matrix.get_states_len()), dtype=bool)
    for i in map(lambda state: second_matrix.index_by_state(state), second_matrix.start_states):
        front[i, :] = front_row_matrix
    return front


def _get_reachable_states(first_matrix: AdjacencyMatrix, second_matrix: AdjacencyMatrix, sub_front_indices, visited) -> Set[State]:
    """
    Helper function to get all reachable indices
    """
    sub_front_offset = sub_front_indices * second_matrix.get_states_len()
    reachable = sparse.csr_matrix((1, first_matrix.get_states_len()), dtype=bool)
    for i in map(lambda state: second_matrix.index_by_state(state), second_matrix.final_states):
        reachable += visited[sub_front_offset + i, :]

    return set(
        first_matrix.state_by_index(i)
        for i in reachable.nonzero()[1]
        if i in map(lambda state: first_matrix.index_by_state(state), first_matrix.final_states)
    )