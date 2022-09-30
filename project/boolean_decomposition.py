import numpy as np
from pyformlang.finite_automaton import Symbol, State, EpsilonNFA
from scipy.sparse import coo_matrix, kron

__all__ = ["BooleanDecomposition", "boolean_decompose_enfa"]


class BooleanDecomposition:
    """
    Class representing boolean decomposition of finite automata
    """

    def __init__(
        self, symbols_to_matrix: dict[Symbol, coo_matrix], states: list[State]
    ):
        """
        :param symbols_to_matrix: dict with mapping symbol on edges to adjacency matrix of these edges
        :param states: states of finite automata
         (adjacency matrices from symbol_to_matrix describes transitions between these states)
        """
        self._symbols_to_matrix = symbols_to_matrix
        self._states_list = states
        states_num = len(states)
        for matrix in symbols_to_matrix.values():
            assert (states_num, states_num) == matrix.get_shape()

    def __eq__(self, other):
        self_dict = self.to_dict()
        other_dict = other.to_dict()
        if not set(self.states()) == set(other.states()):
            return False
        if not set(self_dict.keys()) == set(other_dict.keys()):
            return False
        for i in self_dict.keys():
            nonzero_self = set(zip(*self_dict[i].nonzero()))
            nonzero2_other = set(zip(*other_dict[i].nonzero()))
            if not nonzero_self == nonzero2_other:
                return False
        return True

    def states(self) -> list[State]:
        return self._states_list

    def states_count(self) -> int:
        return len(self._states_list)

    def to_dict(self) -> dict[Symbol, coo_matrix]:
        return self._symbols_to_matrix

    def kron(self, decomposition2: "BooleanDecomposition") -> "BooleanDecomposition":
        """
        Produces kronecker production between matrices with same symbols in boolean decompositions
        :return: boolean decomposition of intersection of finite automatas, represented by decomposition1 and
        decomposition2. States in this decomposition as values have 2 element tuples (state1, state2), where state1 from
        decomposition1, and state2 from decomposition2
        """
        intersection_decomposition = dict()
        dict1 = self.to_dict()
        dict2 = decomposition2.to_dict()
        symbols = set(dict1.keys()).union(set(dict2.keys()))
        for symbol in symbols:
            if symbol in dict1:
                coo_matrix1 = dict1[symbol]
            else:
                coo_matrix1 = coo_matrix((self.states_count(), self.states_count()))

            if symbol in dict2:
                coo_matrix2 = dict2[symbol]
            else:
                coo_matrix2 = coo_matrix(
                    (decomposition2.states_count(), decomposition2.states_count())
                )

            intersection_decomposition[symbol] = kron(coo_matrix1, coo_matrix2)

        intersection_states = list()
        for state1 in self.states():
            for state2 in decomposition2.states():
                intersection_states.append(State((state1, state2)))

        return BooleanDecomposition(intersection_decomposition, intersection_states)

    def transitive_closure(self) -> coo_matrix:
        """
        :return: adjacency matrix of states corresponding to transitive closure
        """
        adjacency_matrix = sum(
            self._symbols_to_matrix.values(),
            coo_matrix((self.states_count(), self.states_count())),
        )

        last_values_count = 0
        while last_values_count != adjacency_matrix.nnz:
            last_values_count = adjacency_matrix.nnz
            adjacency_matrix += adjacency_matrix @ adjacency_matrix

        return adjacency_matrix


def boolean_decompose_enfa(enfa: EpsilonNFA) -> BooleanDecomposition:
    """
    Produce boolean decomposition of EpsilonNFA

    :param enfa: EpsilonNFA to be decomposed
    :return: boolean decomposition of EpsilonNFA
    """
    states_data = list(enfa.states)
    boolean_decompose = dict()
    for (u, symbol_and_vs) in enfa.to_dict().items():
        for (symbol, vs) in symbol_and_vs.items():
            if symbol not in boolean_decompose:
                boolean_decompose[symbol] = list()
            if not type(vs) is set:  # vs is one state in this case
                boolean_decompose[symbol].append(
                    (states_data.index(u), states_data.index(vs))
                )
            else:
                for v in vs:
                    boolean_decompose[symbol].append(
                        (states_data.index(u), states_data.index(v))
                    )

    states_num = len(enfa.states)
    coo_matrices = dict()
    for (symbol, edges) in boolean_decompose.items():
        row = np.array([i for (i, _) in edges])
        col = np.array([j for (_, j) in edges])
        data = np.array([1 for _ in range(len(edges))])
        coo_matrices[symbol] = coo_matrix(
            (data, (row, col)), shape=(states_num, states_num)
        )

    return BooleanDecomposition(coo_matrices, states_data)
