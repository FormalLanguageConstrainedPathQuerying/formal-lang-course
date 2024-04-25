from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
)
from scipy.sparse import dok_matrix, kron, block_diag, csr_matrix
from networkx import MultiDiGraph
from typing import Iterable, Tuple, Set
from project.task2 import graph_to_nfa, regex_to_dfa
from scipy.sparse import dok_matrix, csr_matrix
import pyformlang
from pyformlang.cfg import Epsilon


class FiniteAutomaton:

    basa = None
    start_states = None
    final_states = None
    states_map = None
    flag = True
    nullable_symbols = None  # only produced by rsa_to_mat
    states_count = None  # only produced by rsa_to_mat

    def __init__(
        self,
        obj: any,
        start_states=set(),
        final_states=set(),
        states_map=dict(),
        matrix_class=dok_matrix,
    ):
        if isinstance(obj, DeterministicFiniteAutomaton) or isinstance(
            obj, NondeterministicFiniteAutomaton
        ):
            mat = nfa_to_mat(obj, matrix_class=matrix_class)
            (
                self.basa,
                self.start_states,
                self.final_states,
                self.states_map,
            ) = (mat.basa, mat.start_states, mat.final_states, mat.states_map)
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
        return self.states_map.keys() if self.flag else self.basa.keys()

    def size(self):
        return len(self.states_map)

    def mapOverState_(self, u):
        return self.states_map[State(u)]

    def indexes_dict(self):
        return {i: v for v, i in self.states_map.items()}


def nfa_to_mat(
    automaton: NondeterministicFiniteAutomaton, matrix_class=dok_matrix
) -> FiniteAutomaton:
    states = automaton.to_dict()
    n = len(automaton.states)
    states_map = {v: i for i, v in enumerate(automaton.states)}
    basa = dict()

    for label in automaton.symbols:
        basa[label] = matrix_class((n, n), dtype=bool)
        for u, edges in states.items():
            if label in edges:
                setEdges = (
                    {edges[label]}
                    if not isinstance(edges[label], set)
                    else edges[label]
                )
                for v in setEdges:
                    basa[label][states_map[u], states_map[v]] = True

    res = FiniteAutomaton(
        basa, automaton.start_states, automaton.final_states, states_map
    )
    res.states_count = len(automaton.states)
    return res


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
    automaton1: FiniteAutomaton,
    automaton2: FiniteAutomaton,
    matrix_class_id="csr",
    g=True,
) -> FiniteAutomaton:
    automaton1.flag = not g
    automaton2.flag = not g
    labels = automaton1.labels() & automaton2.labels()
    basa = dict()
    start_states = set()
    final_states = set()
    states_map = dict()

    for label in labels:
        basa[label] = kron(
            automaton1.basa[label], automaton2.basa[label], matrix_class_id
        )

    for u, i in automaton1.states_map.items():
        for v, j in automaton2.states_map.items():
            k = len(automaton2.states_map) * i + j
            states_map[State(k)] = k

            if u in automaton1.start_states and v in automaton2.start_states:
                start_states.add(State(k))

            if u in automaton1.final_states and v in automaton2.final_states:
                final_states.add(State(k))

    return FiniteAutomaton(basa, start_states, final_states, states_map)


def paths_ends(
    graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int], regex: str
) -> list[tuple[object, object]]:
    graph_nfa = nfa_to_mat(graph_to_nfa(graph, start_nodes, final_nodes))
    regex_dfa = nfa_to_mat(regex_to_dfa(regex))
    intersection = intersect_automata(graph_nfa, regex_dfa, g=False)
    closure = transitive_closure(intersection)

    mapping = {v: i for i, v in graph_nfa.states_map.items()}
    result = list()
    for u, v in zip(*closure.nonzero()):
        if u in intersection.start_states and v in intersection.final_states:
            result.append(
                (mapping[u // regex_dfa.size()], mapping[v // regex_dfa.size()])
            )
    return result


def rsm_to_mat(rsm: pyformlang.rsa.RecursiveAutomaton) -> FiniteAutomaton:
    states = set()
    start_states = set()
    final_states = set()
    nullable_symbols = set()

    for var, p in rsm.boxes.items():
        for state in p.dfa.states:
            s = State((var, state.value))
            states.add(s)
            if state in p.dfa.start_states:
                start_states.add(s)
            if state in p.dfa.final_states:
                final_states.add(s)

    len_states = len(states)
    mapping = {v: i for i, v in enumerate(sorted(states, key=lambda x: x.value[1]))}

    m = dict()
    for var, p in rsm.boxes.items():
        for src, transition in p.dfa.to_dict().items():
            for symbol, dst in transition.items():
                label = symbol.value
                if symbol not in m:
                    m[label] = dok_matrix((len_states, len_states), dtype=bool)

                dstSet = {dst} if not isinstance(dst, set) else dst
                for target in dstSet:
                    m[label][
                        mapping[State((var, src.value))],
                        mapping[State((var, target.value))],
                    ] = True
                if isinstance(dst, Epsilon):
                    nullable_symbols.add(label)

    result = FiniteAutomaton(m, start_states, final_states, mapping)
    result.nullable_symbols = nullable_symbols
    result.states_count = len_states
    return result
