from typing import Set, Dict, Union

import pycubool as cb
import scipy.sparse as sps
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, Symbol, State

__all__ = ["BooleanAdjacencies"]


class BooleanAdjacencies:
    """
    Construct a Nondeterministic Finite Automaton boolean adjacency matrices
    by symbols and encapsulates all the information lost in this case.

    Supports CPU and GPU computing platforms.

    Attributes
    ----------
    mode: str, default = "cpu"
        Selected platform used for all calculations
    boolean_adjacencies: Dict[Symbol, Union[sps.dok_matrix, cb.Matrix]]
        Nondeterministic Finite Automaton boolean adjacency matrices by symbols
    states_num: int
        Number of states in specified Nondeterministic Finite Automaton
    shape: Tuple[int, int]
        Adjacency matrix size
    states_nums: Dict[State, int]
        States in specified Nondeterministic Finite Automaton and it's numbers
    nums_states: Dict[int, State]
        Numbers of states in specified Nondeterministic Finite Automaton
        and the states itself
    start_states: Set[State]
        Start states in specified Nondeterministic Finite Automaton
    final_states: Set[State]
        Final states in specified Nondeterministic Finite Automaton
    """

    def __init__(
        self, nfa: NondeterministicFiniteAutomaton = None, mode: str = "cpu"
    ) -> None:
        """
        BooleanAdjacencies class constructor.

        Parameters
        ----------
        nfa: NondeterministicFiniteAutomaton, default = None
            Nondeterministic Finite Automaton to construct boolean adjacency matrices
        mode: str, default = "cpu"
            Allows to select the platform used for all calculations
        """

        modes = ["cpu", "gpu"]
        if mode not in modes:
            raise ValueError("Invalid computing platform specified")
        self.mode = mode

        self.states_num = 0
        self.shape = (self.states_num, self.states_num)
        self.states_nums = dict()
        self.nums_states = dict()
        self.start_states = set()
        self.final_states = set()

        self.boolean_adjacencies = dict()

        if nfa is not None:
            self.states_num = len(nfa.states)
            self.shape = (self.states_num, self.states_num)
            self.states_nums = {state: num for num, state in enumerate(nfa.states)}
            self.nums_states = {num: state for num, state in enumerate(nfa.states)}
            self.start_states = nfa.start_states
            self.final_states = nfa.final_states

            transition_func = nfa.to_dict()
            self.boolean_adjacencies = self._get_boolean_adjacencies(transition_func)

    def _get_boolean_adjacencies(
        self, transition_func: Dict[State, Dict[Symbol, Union[State, Set[State]]]]
    ) -> Dict[Symbol, Union[sps.dok_matrix, cb.Matrix]]:
        """
        Construct a Nondeterministic Finite Automaton boolean adjacency
        matrices by symbols.

        Parameters
        ----------
        transition_func: Dict[State, Dict[Symbol, Union[State, Set[State]]]]
            Transition function of Nondeterministic Finite Automaton

        Returns
        -------
        Dict[Symbol, Union[sps.dok_matrix, cb.Matrix]]
            Nondeterministic Finite Automaton boolean adjacency matrices
            by symbols
        """

        boolean_adjacencies = dict()

        for state_from, transitions in transition_func.items():
            for symbol, states_to in transitions.items():
                if not isinstance(states_to, set):
                    states_to = {states_to}

                for state_to in states_to:
                    state_from_num = self.states_nums[state_from]
                    state_to_num = self.states_nums[state_to]

                    if self.mode == "cpu":
                        if symbol not in boolean_adjacencies:
                            boolean_adjacencies[
                                symbol
                            ]: sps.dok_matrix = sps.dok_matrix(self.shape, dtype=bool)

                        boolean_adjacencies[symbol][state_from_num, state_to_num] = True

                    if self.mode == "gpu":
                        if symbol not in boolean_adjacencies:
                            boolean_adjacencies[symbol]: cb.Matrix = cb.Matrix.empty(
                                self.shape
                            )

                        boolean_adjacencies[symbol][state_from_num, state_to_num] = True

        return boolean_adjacencies

    def intersect(self, other):
        """
        Makes the intersection of two Nondeterministic Finite Automaton
        presented as boolean adjacency matrices by symbols.

        Warnings
        --------
        This method is NOT commutative:
        other should be QUERY Nondeterministic Finite Automaton

        Parameters
        ----------
        other: BooleanAdjacencies
            BooleanAdjacencies of Nondeterministic Finite Automaton
            to intersect with

        Returns
        -------
        BooleanAdjacencies
            The result of intersection presented as
            boolean adjacency matrices by symbols
        """

        intersection = BooleanAdjacencies()
        intersection.mode = self.mode

        intersection.states_num = self.states_num * other.states_num
        intersection.shape = (intersection.states_num, intersection.states_num)
        intersection_symbols = (
            self.boolean_adjacencies.keys() & other.boolean_adjacencies.keys()
        )

        for symbol in intersection_symbols:
            if self.mode == "cpu":
                intersection.boolean_adjacencies[symbol] = sps.kron(
                    self.boolean_adjacencies[symbol],
                    other.boolean_adjacencies[symbol],
                    format="dok",
                )

            if self.mode == "gpu":
                self_boolean_adjacency_indices = self.boolean_adjacencies[
                    symbol
                ].to_lists()
                other_boolean_adjacency_indices = other.boolean_adjacencies[
                    symbol
                ].to_lists()
                intersection.boolean_adjacencies[symbol] = cb.Matrix.from_lists(
                    shape=self.shape,
                    rows=self_boolean_adjacency_indices[0],
                    cols=self_boolean_adjacency_indices[1],
                ).kronecker(
                    cb.Matrix.from_lists(
                        shape=other.shape,
                        rows=other_boolean_adjacency_indices[0],
                        cols=other_boolean_adjacency_indices[1],
                    )
                )

        for graph_state, graph_state_num in self.states_nums.items():
            for query_state, query_state_num in other.states_nums.items():
                intersection_state = State(str(query_state) + "⋂" + str(graph_state))
                intersection_state_num = (
                    graph_state_num * other.states_num + query_state_num
                )

                intersection.states_nums[intersection_state] = intersection_state_num
                intersection.nums_states[intersection_state_num] = intersection_state

                if (
                    graph_state in self.start_states
                    and query_state in other.start_states
                ):
                    intersection.start_states.add(intersection_state)

                if (
                    graph_state in self.final_states
                    and query_state in other.final_states
                ):
                    intersection.final_states.add(intersection_state)

        return intersection

    def get_transitive_closure(self) -> Union[sps.dok_matrix, cb.Matrix]:
        """
        Makes the transitive closure of Nondeterministic Finite Automaton
        presented as boolean adjacency matrices by symbols.

        Returns
        -------
        Union[sps.dok_matrix, cb.Matrix]:
            Nondeterministic Finite Automaton transitive closure
        """

        if self.mode == "cpu":
            transitive_closure: sps.dok_matrix = sps.dok_matrix(
                sps.csr_matrix(
                    sum(
                        boolean_adjacency
                        for boolean_adjacency in self.boolean_adjacencies.values()
                    ),
                    dtype=bool,
                ),
                dtype=bool,
            )

            current_nonzeros = transitive_closure.nnz
            next_nonzeros = 0

            while current_nonzeros != next_nonzeros:
                transitive_closure += transitive_closure @ transitive_closure

                current_nonzeros, next_nonzeros = next_nonzeros, transitive_closure.nnz

            return transitive_closure

        if self.mode == "gpu":
            shape = (0, 0)
            if self.shape == shape:
                shape = (1, 1)
            else:
                shape = self.shape
            transitive_closure: cb.Matrix = cb.Matrix.empty(shape)

            for boolean_adjacency in self.boolean_adjacencies.values():
                boolean_adjacency_indices = boolean_adjacency.to_lists()

                transitive_closure = transitive_closure.ewiseadd(
                    cb.Matrix.from_lists(
                        shape=shape,
                        rows=boolean_adjacency_indices[0],
                        cols=boolean_adjacency_indices[1],
                    )
                )

            current_nonzeros = len(transitive_closure.to_list())
            next_nonzeros = 0

            while current_nonzeros != next_nonzeros:
                transitive_closure_pow: cb.Matrix = transitive_closure.mxm(
                    transitive_closure
                )
                transitive_closure = transitive_closure.ewiseadd(transitive_closure_pow)

                current_nonzeros, next_nonzeros = next_nonzeros, len(
                    transitive_closure.to_list()
                )

            return transitive_closure

    def to_nfa(self) -> NondeterministicFiniteAutomaton:
        """
        Construct a Nondeterministic Finite Automaton from
        it's boolean adjacency matrices by symbols.

        Returns
        -------
        NondeterministicFiniteAutomaton
            The resulting Nondeterministic Finite Automaton
        """

        nfa = NondeterministicFiniteAutomaton()

        for symbol, boolean_adjacency in self.boolean_adjacencies.items():
            if self.mode == "cpu":
                boolean_adjacency_indices = sps.dok_matrix(
                    boolean_adjacency, dtype=bool
                ).nonzero()

                for state_from_num, state_to_num in zip(*boolean_adjacency_indices):
                    state_from = self.nums_states[state_from_num]
                    state_to = self.nums_states[state_to_num]

                    nfa.add_transition(state_from, symbol, state_to)

            if self.mode == "gpu":
                boolean_adjacency_indices = boolean_adjacency.to_lists()

                for state_from_num, state_to_num in zip(*boolean_adjacency_indices):
                    state_from = self.nums_states[state_from_num]
                    state_to = self.nums_states[state_to_num]

                    nfa.add_transition(state_from, symbol, state_to)

        for start_state in self.start_states:
            nfa.add_start_state(start_state)

        for final_state in self.final_states:
            nfa.add_final_state(final_state)

        return nfa
