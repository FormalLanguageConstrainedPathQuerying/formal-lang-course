from typing import Iterable
from networkx import MultiDiGraph
from pyformlang.finite_automaton import *
from pyformlang.rsa import RecursiveAutomaton
from scipy.sparse import dok_matrix, kron
from project.task2 import graph_to_nfa, regex_to_dfa


class FiniteAutomaton:
    start_states = None
    final_states = None
    nfa = None
    lbl = True
    states_mapping = None
    eps = None
    matrix = None

    def __init__(
        self,
        fa: NondeterministicFiniteAutomaton = None,
        *,
        matrix=None,
        start_states=None,
        final_states=None,
        states_to_states=None,
        bad=False,
        eps=None
    ):
        if fa is None:
            self.matrix = matrix
            self.start_states = start_states
            self.final_states = final_states
            self.states_mapping = states_to_states
            self.eps = eps
            if not bad:
                self.nfa = to_nfa(self)
        else:
            self.states_mapping = {v: i for i, v in enumerate(fa.states)}
            self.nfa = fa
            self.matrix = nfa_to_mat(fa, self.states_mapping)
            self.start_states = fa.start_states
            self.final_states = fa.final_states

    def accepts(self, word: Iterable[Symbol]) -> bool:
        return self.nfa.accepts(word)

    def is_empty(self) -> bool:
        return self.nfa.is_empty()

    def size(self):
        return len(self.states_mapping)

    def mapping_for(self, u) -> int:
        return self.states_mapping[State(u)]

    def start_inds(self):
        return [self.mapping_for(t) for t in self.start_states]

    def final_inds(self):
        return [self.mapping_for(t) for t in self.final_states]

    def labels(self):
        return self.states_mapping.keys() if self.lbl else self.matrix.keys()

    def revert_mapping(self):
        return {i: v for v, i in self.states_mapping.items()}


def to_set(state):
    if not isinstance(state, set):
        return {state}
    return state


def nfa_to_mat(fa: NondeterministicFiniteAutomaton, states=None):
    len_states = len(fa.states)
    result = dict()

    for symbol in fa.symbols:
        result[symbol] = dok_matrix((len_states, len_states), dtype=bool)
        for v, edges in fa.to_dict().items():
            if symbol in edges:
                for u in to_set(edges[symbol]):
                    result[symbol][states[v], states[u]] = True

    return result


def rsm_to_fa(rsm: RecursiveAutomaton) -> FiniteAutomaton:
    states = set()
    start_states = set()
    final_states = set()
    epsilons = set()

    for label, enfa in rsm.boxes.items():
        for state in enfa.dfa.states:
            s = State((label, state.value))
            states.add(s)
            if state in enfa.dfa.start_states:
                start_states.add(s)
            if state in enfa.dfa.final_states:
                final_states.add(s)

    len_states = len(states)
    states_to_int = {s: i for i, s in enumerate(states)}

    matrix = dict()
    for label, enfa in rsm.boxes.items():
        for frm, transition in enfa.dfa.to_dict().items():
            for symbol, to in transition.items():
                var = symbol.value
                if symbol not in matrix:
                    matrix[var] = dok_matrix((len_states, len_states), dtype=bool)
                for target in to_set(to):
                    matrix[var][
                        states_to_int[State((label, frm.value))],
                        states_to_int[State((label, target.value))],
                    ] = True
                if isinstance(to, Epsilon):
                    epsilons.add(label)

    return FiniteAutomaton(
        fa=None,
        matrix=matrix,
        start_states=start_states,
        final_states=final_states,
        states_to_states=states_to_int,
        bad=True,
        eps=epsilons,
    )


def to_nfa(fa: FiniteAutomaton):
    nfa = NondeterministicFiniteAutomaton()

    for symbol in fa.matrix.keys():
        matrix_size = fa.matrix[symbol].shape[0]
        for u in range(matrix_size):
            for v in range(matrix_size):
                if fa.matrix[symbol][u, v]:
                    nfa.add_transition(
                        State(fa.states_mapping[State(u)]),
                        symbol,
                        State(fa.states_mapping[State(v)]),
                    )

    for state in fa.start_states:
        nfa.add_start_state(State(fa.states_mapping[State(state)]))
    for state in fa.final_states:
        nfa.add_final_state(State(fa.states_mapping[State(state)]))

    return nfa


def intersect_automata(
    fa1: FiniteAutomaton, fa2: FiniteAutomaton, lbl=True
) -> FiniteAutomaton:
    fa1.lbl = fa2.lbl = not lbl
    labels = fa1.labels() & fa2.labels()
    matrix = dict()
    start_states = set()
    final_states = set()
    states_to_int = dict()

    for label in labels:
        matrix[label] = kron(fa1.matrix[label], fa2.matrix[label], "csr")

    for u, i in fa1.states_mapping.items():
        for v, j in fa2.states_mapping.items():

            k = len(fa2.states_mapping) * i + j
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
        states_to_states=states_to_int,
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
    g_f = FiniteAutomaton(graph_to_nfa(graph, start_nodes, final_nodes))
    r_f = FiniteAutomaton(regex_to_dfa(regex))
    inters = intersect_automata(g_f, r_f, lbl=False)
    close = transitive_closure(inters)
    size = len(r_f.states_mapping)
    r = list()

    for v, u in zip(*close.nonzero()):
        if v in inters.start_states and u in inters.final_states:
            r.append(
                (
                    g_f.states_mapping[v // size],
                    g_f.states_mapping[u // size],
                )
            )
    return r
