from itertools import product
from typing import Iterable
from pyformlang.rsa import RecursiveAutomaton
from networkx import MultiDiGraph
from pyformlang.finite_automaton import *
from scipy.sparse import dok_matrix, kron
from project.task2 import graph_to_nfa, regex_to_dfa


class FiniteAutomaton:
    matrix = None
    start_states = None
    final_states = None
    states_to_int = None
    nfa = None
    states = None

    def __init__(
        self,
        fa: NondeterministicFiniteAutomaton = None,
        *,
        matrix=None,
        start_states=None,
        final_states=None,
        states_to_int=None,
        states=None,
        from_rsm=False,
    ):
        if fa is None:
            self.matrix = matrix
            self.start_states = start_states
            self.final_states = final_states
            self.states_to_int = states_to_int
            self.states = states
            if not from_rsm:
                self.nfa = to_nfa(self)
        else:
            self.states_to_int = {v: i for i, v in enumerate(fa.states)}
            self.nfa = fa
            self.matrix = nfa_to_mat(fa, self.states_to_int)
            self.start_states = fa.start_states
            self.final_states = fa.final_states
            self.states = list(fa.states)

    def accepts(self, word: Iterable[Symbol]) -> bool:
        return self.nfa.accepts(word)

    def is_empty(self) -> bool:
        return self.nfa.is_empty()


def to_set(state):
    if not isinstance(state, set):
        return {state}
    return state


def nfa_to_mat(fa: NondeterministicFiniteAutomaton, states_to_int=None):
    len_states = len(fa.states)
    result = dict()

    for symbol in fa.symbols:
        result[symbol] = dok_matrix((len_states, len_states), dtype=bool)
        for v, edges in fa.to_dict().items():
            if symbol in edges:
                for u in to_set(edges[symbol]):
                    result[symbol][states_to_int[v], states_to_int[u]] = True

    return result


def rsm_to_fa(rsm: RecursiveAutomaton) -> FiniteAutomaton:
    states = [
        (N.value, state.value)
        for N, box in rsm.boxes.items()
        for state in box.dfa.states
    ]

    n_states = len(states)

    mapping = {state: i for i, state in enumerate(states)}

    start_states = {
        (N.value, start_state.value)
        for N, box in rsm.boxes.items()
        for start_state in box.dfa.start_states
    }

    final_states = {
        (N.value, final_state.value)
        for N, box in rsm.boxes.items()
        for final_state in box.dfa.final_states
    }

    matrix = {}
    for N, box in rsm.boxes.items():
        for from_state, transitions in box.dfa.to_dict().items():
            for symbol, to_state in transitions.items():
                from_idx = mapping[(N.value, from_state.value)]
                to_idx = mapping[(N.value, to_state.value)]
                matrix.setdefault(
                    symbol.value, dok_matrix((n_states, n_states), dtype=bool)
                )[from_idx, to_idx] = True

    return FiniteAutomaton(
        fa=None,
        matrix=matrix,
        start_states=start_states,
        final_states=final_states,
        states_to_int=mapping,
        states=states,
        from_rsm=True,
    )


def to_nfa(fa: FiniteAutomaton):
    nfa = NondeterministicFiniteAutomaton()

    for symbol in fa.matrix.keys():
        matrix_size = fa.matrix[symbol].shape[0]
        for u in range(matrix_size):
            for v in range(matrix_size):
                if fa.matrix[symbol][u, v]:
                    nfa.add_transition(
                        State(fa.states_to_int[State(u)]),
                        symbol,
                        State(fa.states_to_int[State(v)]),
                    )

    for state in fa.start_states:
        nfa.add_start_state(State(fa.states_to_int[State(state)]))
    for state in fa.final_states:
        nfa.add_final_state(State(fa.states_to_int[State(state)]))

    return nfa


def intersect_automata(fa1: FiniteAutomaton, fa2: FiniteAutomaton) -> FiniteAutomaton:
    matrix = dict()
    start_states = set()
    final_states = set()
    states_to_int = dict()

    for label in fa1.matrix.keys() & fa2.matrix.keys():
        matrix[label] = kron(fa1.matrix[label], fa2.matrix[label], "csr")

    for u, i in fa1.states_to_int.items():
        for v, j in fa2.states_to_int.items():

            k = len(fa2.states_to_int) * i + j
            states_to_int[k] = k

            if u in fa1.start_states and v in fa2.start_states:
                start_states.add(State(k))

            if u in fa1.final_states and v in fa2.final_states:
                final_states.add(State(k))

    return FiniteAutomaton(
        fa=None,
        matrix=matrix,
        start_states=start_states,
        final_states=final_states,
        states_to_int=states_to_int,
    )


def transitive_closure(fa: FiniteAutomaton):
    if len(fa.matrix.values()) == 0:
        return dok_matrix((0, 0), dtype=bool)

    front = None
    for mat in fa.matrix.values():
        if front is None:
            front = mat
            continue
        front = front + mat
    prev = 0
    while front.count_nonzero() != prev:
        prev = front.count_nonzero()
        front += front @ front

    return front


def paths_ends(
    graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int], regex: str
) -> list[tuple[object, object]]:
    graph_fa = FiniteAutomaton(graph_to_nfa(graph, start_nodes, final_nodes))
    regex_fa = FiniteAutomaton(regex_to_dfa(regex))
    intersect = intersect_automata(graph_fa, regex_fa)
    regex_fa_n = regex_fa.matrix.values().__iter__().__next__().shape[0]

    inter_start_states = {intersect.states_to_int[i] for i in intersect.start_states}
    inter_final_states = {intersect.states_to_int[i] for i in intersect.final_states}

    result = set()
    for state in inter_start_states & inter_final_states:
        n = graph_fa.states[state // regex_fa_n].value
        result.add((n, n))

    if len(intersect.matrix) == 0:
        return list()

    m = sum(intersect.matrix.values())
    for _ in range(m.shape[0]):
        m += m @ m

    for s, f in product(inter_start_states, inter_final_states):
        if m[s, f] != 0:
            result.add(
                (
                    graph_fa.states[s // regex_fa_n].value,
                    graph_fa.states[f // regex_fa_n].value,
                )
            )

    return list(result)
