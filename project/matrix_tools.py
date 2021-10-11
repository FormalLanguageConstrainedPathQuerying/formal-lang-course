from typing import Set, Dict, Union

import scipy.sparse as sps
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, Symbol, State

__all__ = ["BooleanAdjacencies"]


class BooleanAdjacencies:
    """
    Construct a Nondeterministic Finite Automaton boolean adjacency matrices
    by symbols and encapsulates all the information lost in this case.

    Supports only CPU computing platform.

    Attributes
    ----------
    boolean_adjacencies: Dict[Symbol, sps.dok_matrix]
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

    def __init__(self, nfa: NondeterministicFiniteAutomaton = None) -> None:
        """
        BooleanAdjacencies class constructor.

        Parameters
        ----------
        nfa: NondeterministicFiniteAutomaton, default = None
            Nondeterministic Finite Automaton to construct boolean adjacency matrices
        """

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
    ) -> Dict[Symbol, sps.dok_matrix]:
        """
        Construct a Nondeterministic Finite Automaton boolean adjacency
        matrices by symbols.

        Parameters
        ----------
        transition_func: Dict[State, Dict[Symbol, Union[State, Set[State]]]]
            Transition function of Nondeterministic Finite Automaton

        Returns
        -------
        Dict[Symbol, sps.dok_matrix]
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

                    if symbol not in boolean_adjacencies:
                        boolean_adjacencies[symbol]: sps.dok_matrix = sps.dok_matrix(
                            self.shape, dtype=bool
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

        intersection.states_num = self.states_num * other.states_num
        intersection.shape = (intersection.states_num, intersection.states_num)
        intersection_symbols = (
            self.boolean_adjacencies.keys() & other.boolean_adjacencies.keys()
        )

        for symbol in intersection_symbols:
            intersection.boolean_adjacencies[symbol] = sps.kron(
                self.boolean_adjacencies[symbol],
                other.boolean_adjacencies[symbol],
                format="dok",
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

    def get_transitive_closure(self) -> sps.dok_matrix:

        """
        Makes the transitive closure of Nondeterministic Finite Automaton
        presented as boolean adjacency matrices by symbols.

        Returns
        -------
        sps.dok_matrix:
        Nondeterministic Finite Automaton transitive closure
        """

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
            boolean_adjacency_indices = sps.dok_matrix(
                boolean_adjacency, dtype=bool
            ).nonzero()

            for state_from_num, state_to_num in zip(*boolean_adjacency_indices):
                state_from = self.nums_states[state_from_num]
                state_to = self.nums_states[state_to_num]

                nfa.add_transition(state_from, symbol, state_to)

        for start_state in self.start_states:
            nfa.add_start_state(start_state)

        for final_state in self.final_states:
            nfa.add_final_state(final_state)

        return nfa
