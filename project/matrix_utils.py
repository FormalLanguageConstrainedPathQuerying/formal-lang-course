from typing import Dict, Set, Any, List

from pyformlang.finite_automaton import State, EpsilonNFA
from scipy.sparse import dok_matrix, kron, bmat, csr_matrix, lil_array, vstack

__all__ = [
    "BoolMatrixAutomaton",
]


class BoolMatrixAutomaton:
    # Only for internal use
    def __init__(
        self,
        state_to_idx: Dict[State, int],
        start_states: Set[State],
        final_states: Set[State],
        b_mtx: Dict[Any, dok_matrix],
    ):
        """Class represents bool matrix representation of automaton

        Attributes
        ----------

        state_to_idx : Dict[State, int]
            Mapping from states to indices in boolean matrix
        start_states : Set[State]
            Set of start states
        final_states : Set[State]
            Set of final states
        b_mtx: Dict[Any, dok_matrix]
            Mapping from edge label to boolean adjacency matrix
        """
        self.state_to_idx = state_to_idx
        self.start_states = start_states
        self.final_states = final_states
        self.b_mtx = b_mtx

    def __and__(self, other: "BoolMatrixAutomaton") -> "BoolMatrixAutomaton":
        """Calculates intersection of two automatons represented by bool matrices

        Parameters
        ----------
        other : BoolMatrixAutomaton
            The automaton with which intersection will be calculated

        Returns
        -------
        intersection : BoolMatrixAutomaton
            Intersection of two automatons represented by bool matrix
        """
        inter_labels = self.b_mtx.keys() & other.b_mtx.keys()
        inter_b_mtx = {
            label: kron(self.b_mtx[label], other.b_mtx[label]) for label in inter_labels
        }
        inter_state_to_idx = dict()
        inter_start_states = set()
        inter_final_states = set()
        for self_state, self_idx in self.state_to_idx.items():
            for other_state, other_idx in other.state_to_idx.items():
                state = State((self_state.value, other_state.value))
                idx = self_idx * len(other.state_to_idx) + other_idx
                inter_state_to_idx[state] = idx
                if (
                    self_state in self.start_states
                    and other_state in other.start_states
                ):
                    inter_start_states.add(state)
                if (
                    self_state in self.final_states
                    and other_state in other.final_states
                ):
                    inter_final_states.add(state)
        return BoolMatrixAutomaton(
            state_to_idx=inter_state_to_idx,
            start_states=inter_start_states,
            final_states=inter_final_states,
            b_mtx=inter_b_mtx,
        )

    def transitive_closure(self) -> dok_matrix:
        """Calculates transitive closure

        Returns
        -------
        transitive_closure : dok_matrix
            Transitive closure represented by sparse matrix
        """
        transitive_closure = sum(
            self.b_mtx.values(),
            start=dok_matrix((len(self.state_to_idx), len(self.state_to_idx))),
        )
        prev_nnz, cur_nnz = None, transitive_closure.nnz
        if not cur_nnz:
            return transitive_closure
        while prev_nnz != cur_nnz:
            transitive_closure += transitive_closure @ transitive_closure
            prev_nnz, cur_nnz = cur_nnz, transitive_closure.nnz
        return transitive_closure

    @classmethod
    def from_nfa(cls, nfa: EpsilonNFA) -> "BoolMatrixAutomaton":
        """Builds bool matrix from nfa

        Parameters
        ----------
        nfa : EpsilonNFA
            NFA to be converted to bool matrix

        Returns
        -------
        bool_matrix : BoolMatrixAutomaton
            Bool matrix representation of automaton
        """
        state_to_idx = {state: idx for idx, state in enumerate(nfa.states)}
        return cls(
            state_to_idx=state_to_idx,
            start_states=nfa.start_states.copy(),
            final_states=nfa.final_states.copy(),
            b_mtx=cls._b_mtx_from_nfa(
                nfa=nfa,
                state_to_idx=state_to_idx,
            ),
        )

    def to_nfa(self) -> EpsilonNFA:
        """Converts bool matrix representation of automaton to epsilon nfa
        Returns
        -------
        nfa : EpsilonNFA
            Created nfa
        """
        nfa = EpsilonNFA()
        for label, dok_mtx in self.b_mtx.items():
            mtx_as_arr = dok_mtx.toarray()
            for state_from, i in self.state_to_idx.items():
                for state_to, j in self.state_to_idx.items():
                    if mtx_as_arr[i][j]:
                        nfa.add_transition(
                            s_from=state_from,
                            symb_by=label,
                            s_to=state_to,
                        )
        for state in self.start_states:
            nfa.add_start_state(state)
        for state in self.final_states:
            nfa.add_final_state(state)
        return nfa

    @staticmethod
    def _b_mtx_from_nfa(
        nfa: EpsilonNFA, state_to_idx: Dict[State, int]
    ) -> Dict[Any, dok_matrix]:
        """Utility method for creating mapping from labels to adj bool matrix

        Parameters
        ----------
        nfa : EpsilonNFA
            Epsilon NFA from which mapping will be created
        state_to_idx: Dict[State, int]
            Mapping from states to indices in boolean matrix

        Returns
        -------
        b_mtx : Dict[State, int]
            Mapping from labels to adj bool matrix
        """
        b_mtx = dict()
        state_from_to_transition = nfa.to_dict()
        for label in nfa.symbols:
            dok_mtx = dok_matrix((len(nfa.states), len(nfa.states)), dtype=bool)
            for state_from, transitions in state_from_to_transition.items():
                states_to = transitions.get(label, set())
                if not isinstance(states_to, set):
                    states_to = {states_to}
                for state_to in states_to:
                    dok_mtx[state_to_idx[state_from], state_to_idx[state_to]] = True
            b_mtx[label] = dok_mtx
        return b_mtx

    def _direct_sum(self, other: "BoolMatrixAutomaton") -> "BoolMatrixAutomaton":
        """Calculates direct sum of automatons represented by bool matrix

        Parameters
        ----------
        other : BoolMatrixAutomaton
            The matrix with which sum will be calculated

        Returns
        -------
        direct_sum : BoolMatrixAutomaton
            Direct sum
        """
        shifted_state_to_idx = {
            state: len(self.state_to_idx) + idx
            for state, idx in other.state_to_idx.items()
        }
        state_to_idx = {**self.state_to_idx, **shifted_state_to_idx}
        start_states = self.start_states | other.start_states
        final_states = self.final_states | other.final_states
        b_mtx = {
            label: bmat(
                [
                    [self.b_mtx[label], None],
                    [None, other.b_mtx[label]],
                ],
            )
            for label in self.b_mtx.keys() & other.b_mtx.keys()
        }
        return BoolMatrixAutomaton(
            state_to_idx=state_to_idx,
            start_states=start_states,
            final_states=final_states,
            b_mtx=b_mtx,
        )

    def sync_bfs(
        self,
        other: "BoolMatrixAutomaton",
        reachable_per_node: bool,
    ) -> Set[Any]:
        """Executes sync bfs on two automatons represented by bool matrices

        Parameters
        ----------
        other : BoolMatrixAutomaton
            The matrix with which bfs will be executed
        reachable_per_node: bool
            Means calculates reachability for each node separately or not

        Returns
        -------
        result : Set[Any]
            Result depends on reachable_per_node
        if reachable_per_node is false -- set of reachable nodes
        if reachable_per_node is true -- set of tuples (U, V)
        where U is start node and V is final node reachable from U
        """

        if not self.state_to_idx or not other.state_to_idx:
            return set()

        ordered_start_states = list(self.start_states)

        direct_sum = other._direct_sum(self)
        initial_front = self._init_sync_bfs_front(
            other=other,
            reachable_per_node=reachable_per_node,
            ordered_start_states=ordered_start_states,
        )
        front = initial_front
        visited = front.copy()

        other_states_num = len(other.state_to_idx)

        while True:
            visited_nnz = visited.nnz
            new_front = front.copy()

            for _, mtx in direct_sum.b_mtx.items():
                product: csr_matrix = front @ mtx
                new_front_step = lil_array(product.shape)
                for i, j in zip(*product.nonzero()):
                    if j >= other_states_num:
                        continue
                    row = product.getrow(i).tolil()[[0], other_states_num:]
                    if not row.nnz:
                        continue
                    row_shift = i // other_states_num * other_states_num
                    new_front_step[row_shift + j, j] = 1
                    new_front_step[[row_shift + j], other_states_num:] += row
                new_front += new_front_step.tocsr()

            for i, j in zip(*new_front.nonzero()):
                if visited[i, j]:
                    new_front[i, j] = 0

            visited += new_front
            front = new_front

            if visited_nnz == visited.nnz:
                break

        self_idx_to_state = {idx: state for state, idx in self.state_to_idx.items()}
        other_idx_to_state = {idx: state for state, idx in other.state_to_idx.items()}

        result = set()
        nonzero = set(zip(*visited.nonzero())).difference(
            set(zip(*initial_front.nonzero()))
        )
        for i, j in nonzero:
            if (
                other_idx_to_state[i % other_states_num] not in other.final_states
                or j < other_states_num
            ):
                continue
            self_state = self_idx_to_state[j - other_states_num]
            if self_state not in self.final_states:
                continue
            result.add(
                self_state.value
                if not reachable_per_node
                else (
                    ordered_start_states[i // other_states_num].value,
                    self_state.value,
                )
            )
        return result

    def _init_sync_bfs_front(
        self,
        other: "BoolMatrixAutomaton",
        reachable_per_node: bool,
        ordered_start_states: List[State],
    ) -> csr_matrix:
        """Initializes front for sync bfs

        Parameters
        ----------
        other : BoolMatrixAutomaton
            The matrix with which bfs will be executed
        reachable_per_node: bool
            Means calculates reachability for each node separately or not
            ordered_start_states: List[State]
            List of start states

        Returns
        -------
        result : csr_matrix
            Initial front for sync bfs
        """

        def front_with_self_start_row(self_start_row: lil_array):
            front = lil_array(
                (
                    len(other.state_to_idx),
                    len(self.state_to_idx) + len(other.state_to_idx),
                )
            )
            for state in other.start_states:
                idx = other.state_to_idx[state]
                front[idx, idx] = 1
                front[idx, len(other.state_to_idx) :] = self_start_row
            return front

        if not reachable_per_node:
            start_indices = set(
                self.state_to_idx[state] for state in ordered_start_states
            )
            return front_with_self_start_row(
                lil_array(
                    [
                        1 if idx in start_indices else 0
                        for idx in range(len(self.state_to_idx))
                    ]
                )
            ).tocsr()

        fronts = [
            front_with_self_start_row(
                lil_array(
                    [
                        1 if idx == self.state_to_idx[start] else 0
                        for idx in range(len(self.state_to_idx))
                    ]
                )
            )
            for start in ordered_start_states
        ]

        return (
            csr_matrix(vstack(fronts))
            if fronts
            else csr_matrix(
                (
                    len(other.state_to_idx),
                    len(self.state_to_idx) + len(other.state_to_idx),
                )
            )
        )
