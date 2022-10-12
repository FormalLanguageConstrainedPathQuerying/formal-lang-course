from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
import pycubool as cb
from collections.abc import Iterable

__all__ = ["CBBoolDecomposedNFA"]


class CBBoolDecomposedNFA:
    def __init__(self, nfa: NondeterministicFiniteAutomaton = None):
        if nfa is None:
            self.__matrices = {}
            self.__dict = {}
            self.__states_count = 0
            self.__start_vector = None
            self.__final_vector = None
            return
        else:
            CBBoolDecomposedNFA.from_nfa(nfa).move_to(self)

    def take_matrices(self):
        return self.__matrices

    def get_matrices(self):
        res = {}
        for label, matrix in self.__matrices.items():
            res[label] = matrix.dup()
        return res

    def take_dict(self):
        return self.__dict

    def get_dict(self):
        return self.__dict.copy()

    def take_states_count(self):
        return self.__states_count

    def get_states_count(self):
        return self.__states_count

    def take_start_vector(self):
        return self.__start_vector

    def get_start_vector(self):
        if self.__start_vector is None:
            return None
        return self.__start_vector.dup()

    def take_final_vector(self):
        return self.__final_vector

    def get_final_vector(self):
        return self.__final_vector.dup()

    def move_to(self, dest: "CBBoolDecomposedNFA"):
        dest.__matrices = self.__matrices
        dest.__dict = self.__dict
        dest.__states_count = self.__states_count
        dest.__start_vector = self.__start_vector
        dest.__final_vector = self.__final_vector
        return dest

    def copy(self):
        res = CBBoolDecomposedNFA()
        res.__matrices = self.get_matrices()
        res.__dict = self.get_dict()
        res.__states_count = self.get_states_count()
        res.__start_vector = self.get_start_vector()
        res.__final_vector = self.get_final_vector()
        return res

    @staticmethod
    def from_nfa(nfa: NondeterministicFiniteAutomaton = None) -> "CBBoolDecomposedNFA":
        res = CBBoolDecomposedNFA()
        if nfa is None:
            return res
        states_count = len(nfa.states)
        if states_count == 0:
            return res
        res.__matrices = {}
        res.__states_count = states_count
        states = {old: ind for ind, old in enumerate(nfa.states)}
        for start, final_dict in nfa.to_dict().items():
            for label, final_states in final_dict.items():
                if not isinstance(final_states, set):
                    final_states = {final_states}
                for final in final_states:
                    if not label in res.__matrices:
                        res.__matrices[label] = cb.Matrix.empty(
                            shape=(states_count, states_count)
                        )
                    res.__matrices[label][states[start], states[final]] = True
        res.__start_vector = cb.Matrix.empty(shape=(1, states_count))
        res.__final_vector = cb.Matrix.empty(shape=(1, states_count))
        for i in nfa.start_states:
            res.__start_vector[0, states[i]] = True
        for i in nfa.final_states:
            res.__final_vector[0, states[i]] = True
        res.__dict = {v: k for k, v in states.items()}
        return res

    def to_nfa(self) -> NondeterministicFiniteAutomaton:
        res = NondeterministicFiniteAutomaton()
        for label in self.__matrices.keys():
            for start, final in self.__matrices[label].to_list():
                res.add_transition(self.__dict[start], label, self.__dict[final])
        if not self.__start_vector is None:
            for i in self.__start_vector.to_lists()[1]:
                res.add_start_state(self.__dict[i])
        if not self.__final_vector is None:
            for i in self.__final_vector.to_lists()[1]:
                res.add_final_state(self.__dict[i])
        return res

    def __iand__(self, other: "CBBoolDecomposedNFA") -> "CBBoolDecomposedNFA":
        return self.intersect(other).move_to(self)

    def __and__(self, other: "CBBoolDecomposedNFA") -> "CBBoolDecomposedNFA":
        return self.intersect(other)

    def intersect(self, other: "CBBoolDecomposedNFA") -> "CBBoolDecomposedNFA":
        res = CBBoolDecomposedNFA()
        matrices = {}
        intersecting_labels = self.__matrices.keys() & other.__matrices.keys()
        for label in intersecting_labels:
            matrices[label] = self.__matrices[label].kronecker(other.__matrices[label])

        for self_ind, self_node in self.__dict.items():
            for other_ind, other_node in other.__dict.items():
                new_ind = self_ind * other.__states_count + other_ind
                if not isinstance(self_node, Iterable):
                    self_node = [self_node]
                if not isinstance(other_node, Iterable):
                    other_node = [other_node]
                new_node = tuple(list(self_node) + list(other_node))
                res.__dict[new_ind] = new_node

        res.__matrices = matrices
        res.__states_count = self.__states_count * other.__states_count
        if not other.__start_vector is None:
            if not self.__start_vector is None:
                res.__start_vector = self.__start_vector.kronecker(other.__start_vector)
        if not other.__final_vector is None:
            if not self.__final_vector is None:
                res.__final_vector = self.__final_vector.kronecker(other.__final_vector)
        return res

    def transitive_closure(self) -> cb.Matrix:
        if self.__states_count == 0:
            return None
        res = cb.Matrix.empty(shape=(self.__states_count, self.__states_count))
        if len(self.__matrices) == 0:
            return cb.Matrix.empty(shape=(self.__states_count, self.__states_count))

        for m in self.__matrices.values():
            res = res.ewiseadd(m)

        prev_nnz = None
        curr_nnz = res.nvals
        while prev_nnz != curr_nnz:
            res.mxm(res, out=res, accumulate=True)
            prev_nnz = curr_nnz
            curr_nnz = res.nvals

        return res
