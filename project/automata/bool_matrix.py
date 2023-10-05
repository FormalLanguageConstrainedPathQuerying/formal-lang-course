from typing import Hashable

from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State
from scipy import sparse


class BoolMatrix:
    """Represents a bool matrix by nondeterministic
    finite automaton

    This class represents a bool matrix, where epsilon \
    symbols are forbidden.

    Parameters
    ----------
    nfa : NondeterministicFiniteAutomaton, optional
        NFA to initialize bool matrix

    **Attributes:**

    Each bool matrix contains set of states, set of starting states,
    set of final states, and state:index dictionary.
    By default, these are empty but can be filled from the inputted NFA

    """

    def __init__(self, nfa: NondeterministicFiniteAutomaton = None):
        """Initialize a bool matrix with inputted NFA

        Parameters
        ----------
        nfa : NondeterministicFiniteAutomaton, optional
            NFA to initialize bool matrix

        """
        self.start_states, self.final_states = set(), set()
        self.states, self.matrices = dict(), dict()

        if nfa is None:
            return

        for i, state in enumerate(nfa.states):
            self.states[state] = i
        for state in nfa.start_states:
            self.start_states.add(self.states[state])
        for state in nfa.final_states:
            self.final_states.add(self.states[state])

        num_of_states = len(self.states)

        for start_state, transitions in nfa.to_dict().items():
            for symbol, finish_states in transitions.items():
                if isinstance(finish_states, State):
                    finish_states = {finish_states}

                for finish_state in finish_states:
                    if symbol not in self.matrices:
                        self.matrices[symbol] = sparse.csr_matrix(
                            (num_of_states, num_of_states), dtype=bool
                        )

                    self.matrices[symbol][
                        self.states[start_state], self.states[finish_state]
                    ] = True

    def intersect(self, other: "BoolMatrix") -> "BoolMatrix":
        """Intersects a bool matrix with another bool matrix using the tensor product

        Parameters
        ----------
        other : BoolMatrix
            Another bool matrix to intersect

        Returns
        ----------
        result : BoolMatrix
            Matrix equal to tensor product of self and another matrix

        """
        result = BoolMatrix()

        for symbol in self.matrices.keys() & other.matrices.keys():
            result.matrices[symbol] = sparse.kron(
                self.matrices[symbol], other.matrices[symbol], format="csr"
            )

        for self_state, self_index in self.states.items():
            for other_state, other_index in other.states.items():
                result_state = self_index * len(other.states) + other_index
                result.states[(self_state, other_state)] = result_state

                if (
                    self_index in self.start_states
                    and other_index in other.start_states
                ):
                    result.start_states.add(result_state)

                if (
                    self_index in self.final_states
                    and other_index in other.final_states
                ):
                    result.final_states.add(result_state)

        return result

    def transitive_closure(self) -> sparse.csr_matrix:
        """Returns the transitive closure of the given bool matrix

        Returns
        ----------
        result : sparse.csr_matrix
            Transitive closure of bool matrix

        """
        if len(self.matrices) == 0:
            return sparse.csr_matrix((0, 0), dtype=bool)

        num_of_states = len(self.states)
        result = sum(
            self.matrices.values(),
            start=sparse.csr_array((num_of_states, num_of_states), dtype=bool),
        )

        prev_nnz = 0
        while result.nnz != prev_nnz:
            prev_nnz = result.nnz
            result += result @ result

        return result

    def to_nfa(self) -> NondeterministicFiniteAutomaton:
        """Transforms bool matrix into NFA

        Returns
        ----------
        nfa : NondeterministicFiniteAutomaton
            NFA that equivalent to bool matrix

        """
        nfa = NondeterministicFiniteAutomaton()
        for symbol, matrix in self.matrices.items():
            for start_state, finish_state in zip(*matrix.nonzero()):
                nfa.add_transition(start_state, symbol, finish_state)

        for state in self.start_states:
            nfa.add_start_state(state)

        for state in self.final_states:
            nfa.add_final_state(state)

        return nfa

    def direct_sum(self, other: "BoolMatrix") -> "BoolMatrix":
        """Returns a direct sum of bool matrices

        Parameters
        ----------
        other : BoolMatrix
            Another bool matrix to summation

        Returns
        -------
        result : BoolMatrix
            Direct sum of inputted matrices

        """
        result = BoolMatrix()

        for symbol in self.matrices.keys() & other.matrices.keys():
            result.matrices[symbol] = sparse.bmat(
                [
                    [self.matrices[symbol], None],
                    [None, other.matrices[symbol]],
                ]
            )

        ptr = 0
        for state, i in self.states.items():
            result.states[(state, State(0))] = ptr
            if i in self.start_states:
                result.start_states.add(ptr)
            ptr += 1
        for state, i in other.states.items():
            result.states[(state, State(1))] = ptr
            if i in other.start_states:
                result.start_states.add(ptr)
            ptr += 1

        return result

    def build_front_matrix(
        self, other: "BoolMatrix", separate_flag: bool
    ) -> sparse.csr_matrix:
        """Make front csr matrix for bfs

        Parameters
        ----------
        other : BoolMatrix
            Another bool matrix to make front

        separate_flag : bool
            Flag for separated/not separated with start states result

        Returns
        -------
        result : sparse.csr_matrix
            Front csr matrix

        """
        size = (len(other.states), len(self.states) + len(other.states))
        special = sparse.lil_matrix(size)
        self_start_indicators = sparse.lil_array(
            [[i in self.start_states for _, i in self.states.items()]]
        )

        for _, i in other.states.items():
            special[i, i] = True
            special[i, len(other.states) :] = self_start_indicators

        if not self.start_states:
            return sparse.csr_matrix(size)
        if not separate_flag:
            return special.tocsr()

        return sparse.csr_matrix(sparse.vstack([special] * len(self.start_states)))

    @staticmethod
    def validate_front(front: sparse.csr_matrix, bound: int) -> sparse.csr_matrix:
        """Validate front matrix for bfs

        Parameters
        ----------
        front : sparse.csr_matrix
            Original front matrix

        bound : int
            Number of states in bool matrix with transitions in bfs

        Returns
        -------
        validated : sparse.csr_matrix
            Validated front matrix

        """
        validated = sparse.lil_array(front.shape)

        for i, j in zip(*front.nonzero()):
            if j < bound:
                right = front.getrow(i).tolil()[[0], bound:]

                if right.nnz > 0:
                    shift = i // bound * bound
                    validated[shift + j, j] = 1
                    validated[[shift + j], bound:] += right

        return validated.tocsr()

    def bfs(self, other: "BoolMatrix", separate_flag: bool = False) -> set[Hashable]:
        """Returns reachable nodes in self with travelling other
        in two modes: separated (for every start state),
        not separated (for all start state)

        Parameters
        ----------
        other : BoolMatrix
            Another Bool Matrix

        separate_flag : bool
            Separated / not separated mode flag

        Returns
        -------
        result : set[Hashable]
            set[nodes] for not separated mode
            set[(start_node, final_node)] for separated mode

        """
        matrices = self.direct_sum(other).matrices
        symbols = self.matrices.keys() & other.matrices.keys()
        other_states_len = len(other.states)
        self_states_len = len(self.states)

        visited = self.build_front_matrix(other, separate_flag)
        prev = -1
        while visited.nnz != prev:
            prev = visited.nnz

            for symbol in symbols:
                special = visited @ matrices[symbol]
                visited += BoolMatrix.validate_front(special, other_states_len)

        self_start_list = list(self.start_states)
        result = set()
        for i, j in zip(*visited.nonzero()):
            if j >= other_states_len and (i % other_states_len) in other.final_states:
                if (j - other_states_len) in self.final_states:
                    if separate_flag:
                        result.add(
                            (
                                self_start_list[i // self_states_len],
                                j - other_states_len,
                            )
                        )
                    else:
                        result.add(j - other_states_len)

        return result
