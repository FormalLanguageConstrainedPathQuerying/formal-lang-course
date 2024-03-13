from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
)
from scipy.sparse import csr_matrix, kron

from project.task02 import graph_to_nfa, regex_to_dfa
from networkx import MultiDiGraph
from networkx.classes.reportviews import NodeView
from networkx.algorithms.shortest_paths.generic import shortest_path


class FiniteAutomaton:

    def __init__(self, automaton=None, start=None, final=None, state_map=None):
        self.matrix = None
        self.start = set() if start is None else start
        self.final = set() if final is None else final
        self.state_map = dict() if state_map is None else state_map

        if isinstance(
            automaton, (DeterministicFiniteAutomaton, NondeterministicFiniteAutomaton)
        ):
            self.matrix, self.start, self.final, self.state_map = (
                FiniteAutomaton.__from_nfa(automaton)
            )
        else:
            self.matrix = automaton

    def accepts(self, word) -> bool:
        return FiniteAutomaton.__to_nfa(self).accepts(word)

    def is_empty(self) -> bool:
        return not bool(self.matrix)

    @staticmethod
    def __from_nfa(automaton: NondeterministicFiniteAutomaton) -> tuple:
        n = len(automaton.states)
        states = automaton.to_dict()
        state_map = {v: i for i, v in enumerate(automaton.states)}

        matrix = dict()
        for label in automaton.symbols:
            matrix[label] = csr_matrix((n, n), dtype=bool)
            for u, edges in states.items():
                if label in edges:
                    for v in {edges[label]}:
                        matrix[label][state_map[u], state_map[v]] = True

        return matrix, automaton.start_states, automaton.final_states, state_map

    @staticmethod
    def __to_nfa(automaton) -> NondeterministicFiniteAutomaton:
        nfa = NondeterministicFiniteAutomaton()

        for label in automaton.matrix.keys():
            m_size = automaton.matrix[label].shape[0]
            for u in range(m_size):
                for v in range(m_size):
                    if automaton.matrix[label][u, v]:
                        nfa.add_transition(
                            automaton.state_map[u], label, automaton.state_map[v]
                        )

        for s in automaton.start:
            nfa.add_start_state(automaton.state_map[s])
        for s in automaton.final:
            nfa.add_final_state(automaton.state_map[s])

        return nfa


def intersect_automata(a: FiniteAutomaton, b: FiniteAutomaton) -> FiniteAutomaton:
    labels = {label for label in a.matrix.keys() if label in b.matrix}

    automaton = FiniteAutomaton(
        {label: kron(a.matrix[label], b.matrix[label], "csr") for label in labels}
    )

    for u, i in a.state_map.items():
        for v, j in b.state_map.items():

            k = len(b.state_map) * i + j
            automaton.state_map[k] = k

            if u in a.start and v in b.start:
                automaton.start.add(k)

            if u in a.final and v in b.final:
                automaton.final.add(k)

    return automaton


def paths_ends(
    graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int], regex: str
) -> list[tuple[NodeView, NodeView]]:
    automaton_regex = FiniteAutomaton(regex_to_dfa(regex))
    automaton_graph = FiniteAutomaton(graph_to_nfa(graph, start_nodes, final_nodes))
    intersection = intersect_automata(automaton_regex, automaton_graph)
    paths = []
    for start in intersection.start:
        for final in intersection.final:
            try:
                shortest = shortest_path(intersection, start, final)
                paths.append((start, final))
            except:
                pass

    return paths
