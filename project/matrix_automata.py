"""Sparse-matrix finite automata and tensor-based regular path queries."""

from collections.abc import Iterable

from networkx import MultiDiGraph
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State, Symbol
from scipy.sparse import csr_matrix, eye, kron

from project.automata_utils import graph_to_nfa, regex_to_dfa


class AdjacencyMatrixFA:
    """Represent an epsilon-free DFA or NFA by Boolean CSR matrices.

    Each symbol has a matrix whose (i, j) entry denotes a transition from
    state i to state j. Boundary sets contain matrix indices, not original
    state values; ``states`` and ``state_indices`` retain the correspondence.
    """

    def __init__(
        self, automaton: NondeterministicFiniteAutomaton | None = None
    ) -> None:
        self.states = tuple(automaton.states) if automaton is not None else ()
        self.state_indices = {state: i for i, state in enumerate(self.states)}
        self.start_states: set[int] = set()
        self.final_states: set[int] = set()
        self.matrices: dict[Symbol, csr_matrix] = {}
        if automaton is None:
            return

        self.start_states = {self.state_indices[s] for s in automaton.start_states}
        self.final_states = {self.state_indices[s] for s in automaton.final_states}
        coordinates = {}
        for source, transitions in automaton.to_dict().items():
            for symbol, targets in transitions.items():
                # DFA dictionaries store one state, NFA dictionaries a set.
                if isinstance(targets, State):
                    targets = {targets}
                rows, columns = coordinates.setdefault(symbol, ([], []))
                for target in targets:
                    rows.append(self.state_indices[source])
                    columns.append(self.state_indices[target])
        for symbol, (rows, columns) in coordinates.items():
            self.matrices[symbol] = csr_matrix(
                ([True] * len(rows), (rows, columns)),
                shape=(self.num_states, self.num_states),
                dtype=bool,
            )

    @property
    def num_states(self) -> int:
        """Number of states, including isolated ones."""
        return len(self.states)

    def accepts(self, word: Iterable[Symbol]) -> bool:
        """Interpret a word (an iterable of symbols or their raw values)."""
        starts = list(self.start_states)
        current = csr_matrix(
            ([True] * len(starts), ([0] * len(starts), starts)),
            shape=(1, self.num_states),
            dtype=bool,
        )
        for symbol in word:
            matrix = self.matrices.get(Symbol(symbol))
            if matrix is None:
                return False
            current = current @ matrix
            if current.nnz == 0:
                return False
        return bool(self.final_states.intersection(current.indices))

    def transitive_closure(self) -> csr_matrix:
        """Return reflexive reachability by Boolean repeated squaring.

        Including the diagonal accounts for empty words and zero-length paths.
        No dense matrices are created.
        """
        closure = eye(self.num_states, format="csr", dtype=bool)
        for matrix in self.matrices.values():
            closure = closure + matrix
        while True:
            extended = closure + closure @ closure
            if extended.nnz == closure.nnz:
                return extended
            closure = extended

    def is_empty(self) -> bool:
        """Check whether any final state is reachable from a start state."""
        if not self.start_states or not self.final_states:
            return True
        closure = self.transitive_closure()
        return closure[list(self.start_states), :][:, list(self.final_states)].nnz == 0


def intersect_automata(
    automaton1: AdjacencyMatrixFA, automaton2: AdjacencyMatrixFA
) -> AdjacencyMatrixFA:
    """Build the product automaton with a Kronecker product for each label."""
    result = AdjacencyMatrixFA()
    result.states = tuple(
        State((left, right))
        for left in automaton1.states
        for right in automaton2.states
    )
    result.state_indices = {state: i for i, state in enumerate(result.states)}
    width = automaton2.num_states
    result.start_states = {
        left * width + right
        for left in automaton1.start_states
        for right in automaton2.start_states
    }
    result.final_states = {
        left * width + right
        for left in automaton1.final_states
        for right in automaton2.final_states
    }
    for symbol in automaton1.matrices.keys() & automaton2.matrices.keys():
        result.matrices[symbol] = kron(
            automaton1.matrices[symbol], automaton2.matrices[symbol], format="csr"
        )
    return result


def tensor_based_rpq(
    regex: str,
    graph: MultiDiGraph,
    start_nodes: set[int] | None = None,
    final_nodes: set[int] | None = None,
) -> set[tuple[int, int]]:
    """Return graph vertex pairs connected by a word matching ``regex``.

    Omitted or empty boundary sets select all vertices. Paths of length zero
    are allowed when the regular expression accepts the empty word.
    """
    graph_fa = AdjacencyMatrixFA(graph_to_nfa(graph, start_nodes, final_nodes))
    query_fa = AdjacencyMatrixFA(regex_to_dfa(regex))
    product = intersect_automata(graph_fa, query_fa)
    if not product.start_states or not product.final_states:
        return set()
    closure = product.transitive_closure()
    width = query_fa.num_states
    result = set()
    for source in product.start_states:
        for target in closure.getrow(source).indices:
            if target in product.final_states:
                result.add(
                    (
                        graph_fa.states[source // width].value,
                        graph_fa.states[target // width].value,
                    )
                )
    return result
