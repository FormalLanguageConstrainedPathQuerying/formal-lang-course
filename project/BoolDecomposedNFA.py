from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from scipy import sparse
from scipy.sparse import dok_matrix

__all__ = ["BoolDecomposedNFA"]


class BoolDecomposedNFA:
    def __init__(self, nfa: NondeterministicFiniteAutomaton = None):
        if nfa is None:
            self.__matrices = {}
            self.__states_count = 0
            self.__start_vector = dok_matrix((1, 0), dtype=bool)
            self.__final_vector = dok_matrix((1, 0), dtype=bool)
            return
        else:
            BoolDecomposedNFA.from_nfa(nfa).move_to(self)

    def take_matrices(self):
        return self.__matrices

    def get_matrices(self):
        res = {}
        for label, dok in self.__matrices.items():
            res[label] = dok.copy()
        return res

    def take_states_count(self):
        return self.__states_count

    def get_states_count(self):
        return self.__states_count

    def take_start_vector(self):
        return self.__start_vector

    def get_start_vector(self):
        return self.__start_vector.copy()

    def take_final_vector(self):
        return self.__final_vector

    def get_final_vector(self):
        return self.__final_vector.copy()

    def move_to(self, dest: "BoolDecomposedNFA"):
        dest.__matrices = self.__matrices
        dest.__states_count = self.__states_count
        dest.__start_vector = self.__start_vector
        dest.__final_vector = self.__final_vector
        return dest

    def copy(self):
        res = BoolDecomposedNFA()
        res.__matrices = self.get_matrices()
        res.__states_count = self.get_states_count()
        res.__start_vector = self.get_start_vector()
        res.__final_vector = self.get_final_vector()
        return res

    @staticmethod
    def from_nfa(nfa: NondeterministicFiniteAutomaton = None) -> "BoolDecomposedNFA":
        res = BoolDecomposedNFA()
        if nfa is None:
            return res
        states_count = len(nfa.states)
        res.__matrices = {}
        res.__states_count = states_count
        states = {old: ind for ind, old in enumerate(nfa.states)}
        for start, final_dict in nfa.to_dict().items():
            for label, final_states in final_dict.items():
                if not isinstance(final_states, set):
                    final_states = {final_states}
                for final in final_states:
                    if not label in res.__matrices:
                        res.__matrices[label] = dok_matrix(
                            (states_count, states_count), dtype=bool
                        )
                    res.__matrices[label][states[start], states[final]] = True
        res.__start_vector = dok_matrix((1, states_count), dtype=bool)
        res.__final_vector = dok_matrix((1, states_count), dtype=bool)
        for i in nfa.start_states:
            res.__start_vector[0, states[i]] = True
        for i in nfa.final_states:
            res.__final_vector[0, states[i]] = True
        return res

    def to_nfa(self) -> NondeterministicFiniteAutomaton:
        res = NondeterministicFiniteAutomaton()
        for label in self.__matrices:
            for start, final in zip(*self.__matrices[label].nonzero()):
                res.add_transition(start, label, final)
        for i in self.__start_vector.nonzero()[1]:
            res.add_start_state(i)
        for i in self.__final_vector.nonzero()[1]:
            res.add_final_state(i)
        return res

    def __iand__(self, other: "BoolDecomposedNFA") -> "BoolDecomposedNFA":
        return self.intersect(other).move_to(self)

    def __and__(self, other: "BoolDecomposedNFA") -> "BoolDecomposedNFA":
        return self.intersect(other)

    def intersect(self, other: "BoolDecomposedNFA") -> "BoolDecomposedNFA":
        res = BoolDecomposedNFA()
        matrices = {}
        intersecting_labels = self.__matrices.keys() & other.__matrices.keys()
        for label in intersecting_labels:
            matrices[label] = sparse.kron(
                self.__matrices[label], other.__matrices[label]
            )

        res.__matrices = matrices
        res.__states_count = self.__states_count * other.__states_count
        res.__start_vector = sparse.kron(self.__start_vector, other.__start_vector)
        res.__final_vector = sparse.kron(self.__final_vector, other.__final_vector)
        return res

    def transitive_closure(self) -> dok_matrix:
        if len(self.__matrices) == 0:
            return dok_matrix((self.__states_count, self.__states_count), dtype=bool)

        res = sum(self.__matrices.values())
        prev_nnz = None
        curr_nnz = res.nnz
        while prev_nnz != curr_nnz:
            res += res @ res
            prev_nnz = curr_nnz
            curr_nnz = res.nnz
        return res
