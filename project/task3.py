from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
)
from scipy.sparse import dok_matrix, kron, block_diag, csr_matrix
from networkx import MultiDiGraph
from typing import Iterable, Tuple, Set
from project.task2 import graph_to_nfa, regex_to_dfa


class FiniteAutomaton:

    def __init__(
        self, obj: any, start_states=set(), final_states=set(), states_map=dict()
    ):
        if isinstance(obj, DeterministicFiniteAutomaton) or isinstance(
            obj, NondeterministicFiniteAutomaton
        ):
            mat = nfa_to_mat(obj)
            self.basa, self.start_states, self.final_states, self.states_map = (
                mat.basa,
                mat.start_states,
                mat.final_states,
                mat.states_map,
            )
        else:
            self.basa = obj
            self.final_states = final_states
            self.start_states = start_states
            self.states_map = states_map

    def accepts(self, word) -> bool:
        nfa = mat_to_nfa(self)
        real_word = "".join(list(word))
        return nfa.accepts(real_word)

    def is_empty(self) -> bool:
        if isinstance(self.basa, dict):
            return len(self.basa) == 0
        else:
            return self.basa.shape[0] == 0

    def final_idxs(self):
        return [self.mapOverState_(t) for t in self.final_states]

    def start_idxs(self):
        return [self.mapOverState_(t) for t in self.start_states]

    def labels(self):
        return self.states_map.keys()

    def size(self):
        return len(self.states_map)

    def mapOverState_(self, u):
        return self.states_map[State(u)]


def nfa_to_mat(automaton: NondeterministicFiniteAutomaton) -> FiniteAutomaton:
    states = automaton.to_dict()
    n = len(automaton.states)
    states_map = {v: i for i, v in enumerate(automaton.states)}
    basa = dict()

    for label in automaton.symbols:
        basa[label] = dok_matrix((n, n), dtype=bool)
        for u, edges in states.items():
            if label in edges:
                e = edges[label]
                if not isinstance(e, set):
                    e = {e}
                for v in e:
                    basa[label][states_map[u], states_map[v]] = True

    return FiniteAutomaton(
        basa, automaton.start_states, automaton.final_states, states_map
    )


def mat_to_nfa(automaton: FiniteAutomaton) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton()

    for label in automaton.basa.keys():
        n = automaton.basa[label].shape[0]
        for u in range(n):
            for v in range(n):
                if automaton.basa[label][u, v]:
                    nfa.add_transition(
                        automaton.mapOverState_(u),
                        label,
                        automaton.mapOverState_(v),
                    )

    for start_state in automaton.start_states:
        nfa.add_start_state(automaton.mapOverState_(start_state))
    for final_state in automaton.final_states:
        nfa.add_final_state(automaton.mapOverState_(final_state))

    return nfa


def transitive_closure(automaton: FiniteAutomaton):
    if len(automaton.basa.values()) == 0:
        return dok_matrix((0, 0), dtype=bool)
    adj = sum(automaton.basa.values())
    last_ = -1
    while adj.count_nonzero() != last_:
        last_ = adj.count_nonzero()
        adj += adj @ adj

    return adj


def intersect_automata(
    automaton1: FiniteAutomaton, automaton2: FiniteAutomaton
) -> FiniteAutomaton:
    labels = automaton1.basa.keys() & automaton2.basa.keys()
    basa = dict()
    start_states = set()
    final_states = set()
    states_map = dict()

    for label in labels:
        basa[label] = kron(automaton1.basa[label], automaton2.basa[label], "csr")

    for u, i in automaton1.states_map.items():
        for v, j in automaton2.states_map.items():

            k = len(automaton2.states_map) * i + j
            sk = State(k)
            states_map[sk] = k
            assert isinstance(u, State)
            if u in automaton1.start_states and v in automaton2.start_states:
                start_states.add(State(k))

            if u in automaton1.final_states and v in automaton2.final_states:
                final_states.add(State(k))

    return FiniteAutomaton(basa, start_states, final_states, states_map)


def paths_ends(
    graph: MultiDiGraph, start_nodes: Set[int], final_nodes: Set[int], regex: str
):
    graph_fa = nfa_to_mat(graph_to_nfa(graph, start_nodes, final_nodes))

    regex_fa = nfa_to_mat(regex_to_dfa(regex))

    intersected_fa = intersect_automata(graph_fa, regex_fa)

    closure = transitive_closure(intersected_fa)

    paths = []
    map = {v: i for i, v in graph_fa.states_map.items()}
    for start_node, final_node in zip(*closure.nonzero()):
        if (
            start_node in intersected_fa.start_states
            and final_node in intersected_fa.final_states
        ):
            paths.append(
                (map[start_node // regex_fa.size()], map[final_node // regex_fa.size()])
            )

    return paths
