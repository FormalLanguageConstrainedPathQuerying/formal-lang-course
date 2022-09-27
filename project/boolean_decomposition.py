from pyformlang.finite_automaton import Symbol, State
from scipy.sparse import coo_matrix


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
