from scipy.sparse import dok_matrix, kron

from pyformlang.finite_automaton import NondeterministicFiniteAutomaton


class BooleanMatrix:
    """
    Boolean Matrix base class

    Attributes
    ----------
    number_of_states: int
        Number of states
    start_states: Set[int]
        Start states
    final_states: Set[int]
        Final states
    indexed_states: dict
        Renumbered states dictionary
    bmatrix: dict
        Dictionary of boolean matrices.
        Keys are NFA labels
    block_size: int
        Size of a block in boolean matrix
    """

    def __init__(self):
        self.number_of_states = 0
        self.start_states = set()
        self.final_states = set()
        self.indexed_states = {}
        self.bmatrix = {}
        self.block_size = 1

    def transitive_closure(self):
        """
        Computes transitive closure of boolean matrices

        Returns
        -------
        tc: dok_matrix
            Transitive closure of boolean matrices
        """
        if not self.bmatrix.values():
            return dok_matrix((1, 1))

        tc = sum(self.bmatrix.values())

        prev_nnz = tc.nnz
        curr_nnz = 0

        while prev_nnz != curr_nnz:
            tc += tc @ tc
            prev_nnz, curr_nnz = curr_nnz, tc.nnz

        return tc

    @classmethod
    def from_nfa(cls, nfa: NondeterministicFiniteAutomaton):
        """
        Transforms NFA into BooleanMatrix

        Parameters
        ----------
        nfa: NondeterministicFiniteAutomaton
            NFA to transform
        Returns
        -------
        obj: BooleanMatrix
            BooleanMatrix object from NFA
        """
        obj = cls()
        obj.number_of_states = len(nfa.states)
        obj.indexed_states = {state: idx for idx, state in enumerate(nfa.states)}
        obj.start_states, obj.final_states = nfa.start_states, nfa.final_states
        obj.bmatrix = obj._nfa_to_bmatrix(nfa)
        return obj

    def _nfa_to_bmatrix(self, nfa: NondeterministicFiniteAutomaton):
        """
        Parameters
        ----------
        nfa: NondeterministicFiniteAutomaton
            NFA to transform to matrix

        Returns
        -------
        bmatrix: dict
            Dict of boolean matrix for every automata label-key
        """
        bmatrix = dict()
        nfa_dict = nfa.to_dict()
        for label in nfa.symbols:
            tmp_matrix = dok_matrix((len(nfa.states), len(nfa.states)), dtype=bool)
            for state_from, transitions in nfa_dict.items():
                if label in transitions:
                    states_to = (
                        transitions[label]
                        if isinstance(transitions[label], set)
                        else {transitions[label]}
                    )
                    for state_to in states_to:
                        tmp_matrix[
                            self.indexed_states[state_from],
                            self.indexed_states[state_to],
                        ] = True
            bmatrix[label] = tmp_matrix
        return bmatrix

    def intersect(self, other):
        """
        Computes intersection of self boolean matrix with other

        Parameters
        ----------
        other: NFAMatrix
            Right-hand side boolean matrix
        Returns
        -------
        intersection: NFAMatrix
            Intersection of two boolean matrices
        """
        intersection = self.__class__()
        common_labels = self.bmatrix.keys() & other.bmatrix.keys()

        for label in common_labels:
            intersection.bmatrix[label] = kron(
                self.bmatrix[label], other.bmatrix[label], format="dok"
            )

        for state_lhs, s_lhs_index in self.indexed_states.items():
            for state_rhs, s_rhs_index in other.indexed_states.items():
                new_state = new_state_idx = (
                    s_lhs_index * len(other.indexed_states) + s_rhs_index
                )
                intersection.indexed_states[new_state] = new_state_idx

                if state_lhs in self.start_states and state_rhs in other.start_states:
                    intersection.start_states.add(new_state)

                if state_lhs in self.final_states and state_rhs in other.final_states:
                    intersection.final_states.add(new_state)

        return intersection
