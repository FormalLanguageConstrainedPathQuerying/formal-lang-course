import numpy as np
import scipy.sparse as sp
import functools
from networkx import MultiDiGraph
from collections.abc import Iterable
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, Symbol
from project import t2_fa_utils as t2


class AdjacencyMatrixFA:
    n_states: int
    """Number of states in the automaton"""

    transitions: dict[Symbol, sp.csr_matrix]
    """Dictionary mapping symbols to sparse adjacency matrices (CSR)"""

    start_states: np.ndarray
    """Boolean vector marking start states"""

    final_states: np.ndarray
    """Boolean vector marking final states"""

    alphabet: set[Symbol]
    """Alphabet of the automaton"""

    def __init__(self, nfa: NondeterministicFiniteAutomaton):
        states = list(nfa.states)
        index = {s: i for i, s in enumerate(states)}
        self.n_states = len(states)

        transitions = {a: [] for a in nfa.symbols}

        for s_from, symb, s_to in nfa._transition_function.get_edges():
            i = index[s_from]
            j = index[s_to]
            transitions[symb].append((i, j))

        self.transitions = {}
        for a, edges in transitions.items():
            if edges:
                rows, cols = zip(*edges)
                data = np.ones(len(edges), dtype=bool)
                mat = sp.csr_matrix(
                    (data, (rows, cols)), shape=(self.n_states, self.n_states)
                )
            else:
                mat = sp.csr_matrix((self.n_states, self.n_states), dtype=bool)
            self.transitions[a] = mat

        self.start_states = np.zeros(self.n_states, dtype=bool)
        for s in nfa.start_states:
            self.start_states[index[s]] = True

        self.final_states = np.zeros(self.n_states, dtype=bool)
        for s in nfa.final_states:
            self.final_states[index[s]] = True

        self.alphabet = nfa.symbols

    @classmethod
    def from_components(
        cls,
        n_states: int,
        alphabet,
        transitions: dict,
        start_states: np.ndarray,
        final_states: np.ndarray,
    ):
        obj = cls.__new__(cls)
        obj.n_states = n_states
        obj.alphabet = set(alphabet)
        obj.transitions = transitions
        obj.start_states = start_states
        obj.final_states = final_states
        return obj

    def transitive_closure(self) -> sp.csc_matrix:
        """
        Compute the transitive closure of the adjacency matrix of the automaton
        Returns boolean matrix T where T[i, j] = True if j is reachable from i.
        """
        n = self.n_states

        matrices = list(self.transitions.values())
        if matrices:
            adj_matrix = functools.reduce(lambda x, y: x + y, matrices)
            adj_matrix.data = np.ones_like(adj_matrix.data, dtype=bool)
        else:
            adj_matrix = sp.csr_matrix((n, n), dtype=bool)

        adj_matrix = adj_matrix + sp.identity(n, dtype=bool, format="csr")

        result = adj_matrix.copy()
        for _ in range(n - 1):
            result = (result @ adj_matrix).astype(bool)

        return result

    def accepts(self, word: Iterable[Symbol]) -> bool:
        current_states = set(np.where(self.start_states)[0])

        for symbol in word:
            if symbol not in self.transitions:
                return False

            next_states = set()
            mat = self.transitions[symbol].tocoo()
            for i, j in zip(mat.row, mat.col):
                if i in current_states:
                    next_states.add(j)

            current_states = next_states
            if not current_states:
                return False

        final_indices = set(np.where(self.final_states)[0])
        return bool(current_states & final_indices)

    def is_empty(self) -> bool:
        """
        Check if the language of the automaton is empty.
        Returns True if no final state is reachable from any start state.
        """
        tr_cl = self.transitive_closure()

        start_indices = np.where(self.start_states)[0]
        final_indices = np.where(self.final_states)[0]

        for i in start_indices:
            for j in final_indices:
                if tr_cl[i, j]:
                    return False

        return True


def intersect_automata(
    automaton1: AdjacencyMatrixFA, automaton2: AdjacencyMatrixFA
) -> AdjacencyMatrixFA:
    total_alph = automaton1.alphabet & automaton2.alphabet
    n = automaton1.n_states * automaton2.n_states

    total_transitions = {}
    for sym in total_alph:
        total_transitions[sym] = sp.kron(
            automaton1.transitions[sym], automaton2.transitions[sym], format="csr"
        )

    total_ss = np.kron(
        automaton1.start_states.astype(int), automaton2.start_states.astype(int)
    ).astype(bool)

    total_fs = np.kron(
        automaton1.final_states.astype(int), automaton2.final_states.astype(int)
    ).astype(bool)

    return AdjacencyMatrixFA.from_components(
        n, total_alph, total_transitions, total_ss, total_fs
    )


def tensor_based_rpq(
    regex: str, graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int]
) -> set[tuple[int, int]]:
    g_nfa = t2.graph_to_nfa(graph, start_nodes, final_nodes)
    g_amfa = AdjacencyMatrixFA(g_nfa)

    r_dfa = t2.regex_to_dfa(regex)
    r_amfa = AdjacencyMatrixFA(r_dfa)

    # get only paths we need (mutual)
    i_amfa = intersect_automata(g_amfa, r_amfa)

    # get reachability
    tr = i_amfa.transitive_closure()

    prod_starts = np.where(i_amfa.start_states)[0]
    prod_finals = np.where(i_amfa.final_states)[0]

    g_states = list(g_nfa.states)
    r_n = r_amfa.n_states

    result: set[tuple[int, int]] = set()

    for p in prod_starts:
        for q in prod_finals:
            if tr[p, q]:
                g_p_idx = p // r_n
                g_q_idx = q // r_n
                u = g_states[g_p_idx]
                v = g_states[g_q_idx]
                result.add((u, v))

    return result
