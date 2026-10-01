from collections import defaultdict
from collections.abc import Iterable

from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State, Symbol
from scipy.sparse import csr_matrix, eye, kron


class AdjacencyMatrixFA:
    """
    Finite automaton represented by a boolean sparse matrix for each symbol.

    Attributes:
        states: Original states in matrix row and column order, including isolated states.
        start_states: Indices of initial states in states.
        final_states: Indices of accepting states in states.
        matrices: Symbol-to-matrix mapping. Entry (i, j) is true when the automaton
            has a transition from states[i] to states[j] on that symbol.
    """

    def __init__(self, automaton: NondeterministicFiniteAutomaton) -> None:
        """
        Build a matrix representation of a DFA or an NFA without epsilon transitions.

        Args:
            automaton: Automaton to convert. Its states and transitions are copied.
        """
        states = tuple(automaton.states)
        indices = {state: index for index, state in enumerate(states)}
        start_states = {indices[state] for state in automaton.start_states}
        final_states = {indices[state] for state in automaton.final_states}

        transitions = defaultdict(list)
        for source, symbol, target in automaton:
            transitions[symbol].append((indices[source], indices[target]))

        matrices = {}
        for symbol, edges in transitions.items():
            rows, columns = zip(*edges)
            matrices[symbol] = csr_matrix(
                ([True] * len(edges), (rows, columns)),
                shape=(len(states), len(states)),
                dtype=bool,
            )

        self._initialize(states, start_states, final_states, matrices)

    def _initialize(
        self,
        states: tuple[State, ...],
        start_states: set[int],
        final_states: set[int],
        matrices: dict[Symbol, csr_matrix],
    ) -> None:
        """Store components using one common ordering of states."""
        self.states = states
        self.start_states = start_states
        self.final_states = final_states
        self.matrices = matrices

    @classmethod
    def _from_matrices(
        cls,
        states: tuple[State, ...],
        start_states: set[int],
        final_states: set[int],
        matrices: dict[Symbol, csr_matrix],
    ) -> "AdjacencyMatrixFA":
        """Build from already computed boolean CSR matrices and matching indices."""
        automaton = cls.__new__(cls)
        automaton._initialize(states, start_states, final_states, matrices)
        return automaton

    @property
    def num_states(self) -> int:
        """Number of states, including isolated states."""
        return len(self.states)

    def accepts(self, word: Iterable[Symbol]) -> bool:
        """
        Check whether the automaton accepts a word.

        Args:
            word: Iterable of symbols or their raw values. A multicharacter label
                is one symbol; an empty iterable represents the empty word.

        Returns:
            bool: Whether the word leads from an initial state to an accepting state.
        """
        current = csr_matrix(
            (
                [True] * len(self.start_states),
                ([0] * len(self.start_states), list(self.start_states)),
            ),
            shape=(1, self.num_states),
            dtype=bool,
        )
        for symbol in word:
            if not isinstance(symbol, Symbol):
                symbol = Symbol(symbol)
            matrix = self.matrices.get(symbol)
            if matrix is None:
                return False
            current = current @ matrix
            if current.nnz == 0:
                return False

        return bool(self.final_states.intersection(current.indices))

    def transitive_closure(self) -> csr_matrix:
        """
        Compute reachability between all pairs of states, ignoring transition labels.

        Note:
            The closure is reflexive: every state reaches itself via the empty path.
            Repeated boolean squaring doubles the maximum path length each round.

        Returns:
            csr_matrix: Boolean matrix in the same state order as the transition matrices.
        """
        closure = eye(self.num_states, format="csr", dtype=bool)
        for matrix in self.matrices.values():
            closure = closure + matrix

        while True:
            expanded = closure + closure @ closure
            if expanded.nnz == closure.nnz:
                return expanded
            closure = expanded

    def is_empty(self) -> bool:
        """
        Check whether the language of the automaton is empty.

        Returns:
            bool: True if no accepting state is reachable from any initial state,
                including paths of length zero.
        """
        if not self.start_states or not self.final_states:
            return True
        if self.start_states & self.final_states:
            return False
        closure = self.transitive_closure()
        return closure[list(self.start_states)][:, list(self.final_states)].nnz == 0


def intersect_automata(
    automaton1: AdjacencyMatrixFA, automaton2: AdjacencyMatrixFA
) -> AdjacencyMatrixFA:
    """
    Intersect two automata using the Kronecker product of their transition matrices.

    Note:
        Only transitions with the same symbol are synchronized. Product state (i, j)
        has index i * automaton2.num_states + j, matching scipy.sparse.kron.

    Args:
        automaton1: First automaton. It is not modified.
        automaton2: Second automaton. It is not modified.

    Returns:
        AdjacencyMatrixFA: Automaton accepting exactly the words accepted by both
            inputs. Each state value is a pair of the corresponding input state values.
    """
    states = tuple(
        State((left.value, right.value))
        for left in automaton1.states
        for right in automaton2.states
    )
    start_states = {
        left * automaton2.num_states + right
        for left in automaton1.start_states
        for right in automaton2.start_states
    }
    final_states = {
        left * automaton2.num_states + right
        for left in automaton1.final_states
        for right in automaton2.final_states
    }
    matrices = {
        symbol: kron(
            automaton1.matrices[symbol], automaton2.matrices[symbol], format="csr"
        )
        for symbol in automaton1.matrices.keys() & automaton2.matrices.keys()
    }
    return AdjacencyMatrixFA._from_matrices(
        states, start_states, final_states, matrices
    )
