from typing import Optional, Iterable
from pyformlang.finite_automaton import Symbol
import numpy as np
from networkx import MultiDiGraph
from typing import Any
from scipy import sparse
from itertools import product
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from project.hw2.graph_to_nfa_tool import graph_to_nfa
from project.hw2.regex_to_dfa_tool import regex_to_dfa


class AdjacencyMatrixFA:
    states_cnt: int
    adjacent_vertices: dict  # stores pairs of nodes that connected by an edge
    labeled_node_numbers: dict[
        Any, int
    ]  # stores key: value structure, key - node label, value - node index
    boolean_decomposition: dict[Any, sparse.csr_matrix]
    start_states: set
    final_states: set

    def __init__(self, automata: Optional[NondeterministicFiniteAutomaton] = None):
        if automata is None:
            self.adjacent_vertices = {}
            self.labeled_node_numbers = {}
            self.boolean_decomposition = {}
            self.states_cnt = 0
            self.start_states = set()
            self.finish_states = set()
            return

        graph = automata.to_networkx()
        self.labeled_node_numbers = {}
        self.adjacent_vertices = {}
        self.boolean_decomposition = {}

        for ind, el in enumerate(graph.nodes()):
            self.labeled_node_numbers[el] = ind

        self.start_states = {
            self.labeled_node_numbers.get(el) for el in automata.start_states
        }
        self.final_states = {
            self.labeled_node_numbers.get(el) for el in automata.final_states
        }
        self.states_cnt = graph.number_of_nodes()

        labels = set()
        edges = graph.edges(data="label")
        for edge in edges:
            first_state = edge[0]
            second_state = edge[1]
            label = edge[2]
            if label is not None:
                self.adjacent_vertices.setdefault(label, [])
                self.adjacent_vertices[label].append((first_state, second_state))
                labels.add(label)

        for label in labels:
            data = np.ones(len(self.adjacent_vertices[label]), dtype=bool)
            rows = []
            columns = []
            for el in self.adjacent_vertices[label]:
                rows.append(self.labeled_node_numbers[el[0]])
                columns.append(self.labeled_node_numbers[el[1]])
            decomposition = sparse.csr_matrix(
                (data, (rows, columns)), shape=(self.states_cnt, self.states_cnt)
            )
            self.boolean_decomposition[label] = decomposition

    def transitive_closure(self):
        if not self.boolean_decomposition:
            return np.eye(len(self.labeled_node_numbers), dtype=bool)
        adjacency_matrix = sum(self.boolean_decomposition.values())
        adjacency_matrix.setdiag(True)
        res = np.linalg.matrix_power(
            adjacency_matrix.toarray(), len(self.labeled_node_numbers)
        )
        return res

    def accepts(self, word: Iterable[Symbol]) -> bool:
        cur_states = self.start_states.copy()
        for el in word:
            if el not in self.boolean_decomposition.keys():
                return False
            cur_states = set()
            for cur_state, next_state in product(
                cur_states, self.labeled_node_numbers.values()
            ):
                if self.boolean_decomposition[el][cur_state, next_state]:
                    cur_states.add(next_state)
        for state in cur_states:
            if state in self.final_states:
                continue
            else:
                return False
        return True

    def is_empty(self) -> bool:
        t = self.transitive_closure()
        st = False
        for s in self.start_states:
            for f in self.final_states:
                if t[s, f]:
                    st = True
        if st:
            return False
        else:
            return True


def intersect_automata(
    automaton1: AdjacencyMatrixFA, automaton2: AdjacencyMatrixFA
) -> AdjacencyMatrixFA:
    intersection_boolean_decompositions = {}
    intersection_nodes = {}
    start_nodes = set()
    final_nodes = set()
    intersect_labels = (
        automaton1.boolean_decomposition.keys()
        & automaton2.boolean_decomposition.keys()
    )

    for lab in intersect_labels:
        intersection_boolean_decompositions[lab] = sparse.kron(
            automaton1.boolean_decomposition[lab],
            automaton2.boolean_decomposition[lab],
            format="csr",
        )

    for node1, node2 in product(
        automaton1.labeled_node_numbers.keys(), automaton2.labeled_node_numbers.keys()
    ):
        intersection_nodes[(node1, node2)] = (
            automaton1.labeled_node_numbers[node1] * automaton2.states_cnt
            + automaton2.labeled_node_numbers[node2]
        )

    for pair_nodes, index in intersection_nodes.items():
        if (
            automaton1.labeled_node_numbers[pair_nodes[0]] in automaton1.start_states
            and automaton2.labeled_node_numbers[pair_nodes[1]]
            in automaton2.start_states
        ):
            start_nodes.add(index)
        if (
            automaton1.labeled_node_numbers[pair_nodes[0]] in automaton1.final_states
            and automaton2.labeled_node_numbers[pair_nodes[1]]
            in automaton2.final_states
        ):
            final_nodes.add(index)
    intersection = AdjacencyMatrixFA()
    intersection.start_states = start_nodes
    intersection.final_states = final_nodes
    intersection.boolean_decomposition = intersection_boolean_decompositions
    intersection.states_cnt = automaton1.states_cnt * automaton2.states_cnt
    intersection.labeled_node_numbers = intersection_nodes
    return intersection


def tensor_based_rpq(
    regex: str, graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int]
) -> set[tuple[int, int]]:
    rex_dfa = regex_to_dfa(regex)
    nfa = graph_to_nfa(graph, start_nodes, final_nodes)
    rex_fa = AdjacencyMatrixFA(rex_dfa)
    g_fa = AdjacencyMatrixFA(nfa)
    inter = intersect_automata(g_fa, rex_fa)
    inter_tc = inter.transitive_closure()
    res = set()
    for start_g in start_nodes:
        for final_g in final_nodes:
            for start_r in rex_dfa.start_states:
                for final_r in rex_dfa.final_states:
                    if inter_tc[
                        inter.labeled_node_numbers[(start_g, start_r)],
                        inter.labeled_node_numbers[(final_g, final_r)],
                    ]:
                        res.add((start_g, final_g))
    return res
