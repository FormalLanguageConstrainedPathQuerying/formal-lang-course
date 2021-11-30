from abc import ABC, abstractmethod

from pyformlang.cfg import Variable
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State

from project.grammars.rsm import RSM
from project.grammars.rsm_box import RSMBox


class BooleanMatrix(ABC):
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
        self.states_to_box_variable = {}

    # def transitive_closure(self):
    #     """
    #     Computes transitive closure of boolean matrices
    #
    #     Returns
    #     -------
    #     tc: dok_matrix
    #         Transitive closure of boolean matrices
    #     """
    #     if not self.bmatrix.values():
    #         return dok_matrix((1, 1))
    #
    #     tc = sum(self.bmatrix.values())
    #
    #     prev_nnz = tc.nnz
    #     curr_nnz = 0
    #
    #     while prev_nnz != curr_nnz:
    #         tc += tc @ tc
    #         prev_nnz, curr_nnz = curr_nnz, tc.nnz
    #
    #     return tc

    def get_nonterminals(self, s_from, s_to):
        return self.states_to_box_variable.get((s_from, s_to))

    @classmethod
    def from_rsm(cls, rsm: RSM):
        """
        Create an instance of RSMMatrix from rsm

        Attributes
        ----------
        rsm: RSM
            Recursive State Machine
        """
        bm = cls()
        bm.number_of_states = sum(len(box.dfa.states) for box in rsm.boxes)
        box_idx = 0
        for box in rsm.boxes:
            for idx, state in enumerate(box.dfa.states):
                new_name = bm._rename_rsm_box_state(state, box.variable)
                bm.indexed_states[new_name] = idx + box_idx
                if state in box.dfa.start_states:
                    bm.start_states.add(bm.indexed_states[new_name])
                if state in box.dfa.final_states:
                    bm.final_states.add(bm.indexed_states[new_name])

            bm.states_to_box_variable.update(
                {
                    (
                        bm.indexed_states[
                            bm._rename_rsm_box_state(box.dfa.start_state, box.variable)
                        ],
                        bm.indexed_states[
                            bm._rename_rsm_box_state(state, box.variable)
                        ],
                    ): box.variable.value
                    for state in box.dfa.final_states
                }
            )
            bm.bmatrix.update(bm._create_box_bool_matrices(box))
            box_idx += len(box.dfa.states)

        return bm

    def _create_box_bool_matrices(self, box: RSMBox) -> dict:
        """
        Create bool matrices for RSM box

        Attributes
        ----------
        box: RSMBox
            Box of RSM

        Returns
        -------
        bmatrix: dict
            Boolean Matrices dict
        """
        bmatrix = {}
        for s_from, trans in box.dfa.to_dict().items():
            for label, states_to in trans.items():
                if not isinstance(states_to, set):
                    states_to = {states_to}
                for s_to in states_to:
                    idx_from = self.indexed_states[
                        self._rename_rsm_box_state(s_from, box.variable)
                    ]
                    idx_to = self.indexed_states[
                        self._rename_rsm_box_state(s_to, box.variable)
                    ]
                    label = str(label)
                    if label in self.bmatrix:
                        self.bmatrix[label][idx_from, idx_to] = True
                        continue
                    if label not in bmatrix:
                        bmatrix[label] = self._create_bool_matrix(
                            (self.number_of_states, self.number_of_states)
                        )
                    bmatrix[label][idx_from, idx_to] = True

        return bmatrix

    @staticmethod
    def _rename_rsm_box_state(state: State, box_variable: Variable):
        return State(f"{state.value}#{box_variable.value}")

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
            tmp_matrix = self._create_bool_matrix((len(nfa.states), len(nfa.states)))
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

    def to_nfa(self):
        """
        Transforms BooleanMatrix into NFA

        Returns
        -------
        nfa: NondeterministicFiniteAutomaton
            Representation of BooleanMatrix as NFA
        """
        nfa = NondeterministicFiniteAutomaton()
        for label in self.bmatrix.keys():
            arr = self.bmatrix[label].toarray()
            for i in range(len(arr)):
                for j in range(len(arr)):
                    if arr[i][j]:
                        from_state = (
                            State((i // self.block_size, i % self.block_size))
                            if self.block_size > 1
                            else State(i)
                        )
                        to_state = (
                            State((j // self.block_size, j % self.block_size))
                            if self.block_size > 1
                            else State(j)
                        )
                        nfa.add_transition(
                            self.indexed_states[from_state],
                            label,
                            self.indexed_states[to_state],
                        )

        for start_state in self.start_states:
            nfa.add_start_state(self.indexed_states[State(start_state)])
        for final_state in self.final_states:
            nfa.add_final_state(self.indexed_states[State(final_state)])

        return nfa

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
        intersection.number_of_states = self.number_of_states * other.number_of_states
        common_labels = self.bmatrix.keys() & other.bmatrix.keys()

        for label in common_labels:
            intersection.bmatrix[label] = self._kron(
                self.bmatrix[label], other.bmatrix[label]
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

    @staticmethod
    @abstractmethod
    def _kron(bm1, bm2):
        pass

    @staticmethod
    @abstractmethod
    def _get_nonzero(bm):
        pass

    @staticmethod
    @abstractmethod
    def _create_bool_matrix(shape):
        pass
