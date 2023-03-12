from project.fa_utils import regex2dfa, graph2nfa
from pyformlang.finite_automaton import EpsilonNFA
import networkx as nx
import numpy as np
from scipy.sparse import dok_matrix, kron

from pyformlang.finite_automaton import EpsilonNFA

from typing import Tuple, Dict


def fa2matrix(fa: EpsilonNFA) -> Tuple[Dict, Dict]:
    """
    Builds a dictionary of matrices for a given finite automaton

    Args:
        fa: Epsilon non-deterministic finite automaton

    Returns:
        Tuple of two dictionaries:
        transition matrices for characters and automaton states ids for state labels
    """

    matrix = {}

    states_mapping = {s: i for i, s in enumerate(fa.states)}

    for source, label, dest in fa:
        if label not in matrix:
            matrix[label] = dok_matrix((len(fa.states), len(fa.states)), dtype=np.bool_)
        matrix[label][states_mapping[source], states_mapping[dest]] = True

    return (matrix, states_mapping)


def intersect_nfa(fa1: EpsilonNFA, fa2: EpsilonNFA) -> EpsilonNFA:
    """
    Builds intersection of two given finite automatons.

    Args:
        fa1: Finite automaton
        fa2: Another finite automaton

    Returns:
        Intersection of two finite automatons
    """
    matrix1, map1 = fa2matrix(fa1)
    matrix2, map2 = fa2matrix(fa2)

    krons = {
        label: kron(matrix1[label], matrix2[label])
        for label in set(matrix1.keys()).intersection(set(matrix2.keys()))
    }

    ans = EpsilonNFA()

    for label in krons:
        for source, dest, val in zip():
            if val:
                ans.add_transition(source, label, dest)

    for symb, mat in krons.items():
        from_idx, to_idx = mat.nonzero()
        for fro, to in zip(from_idx, to_idx):
            ans.add_transition(fro, symb, to)

    for start_state1 in fa1.start_states:
        for start_state2 in fa2.start_states:
            ans.add_start_state(map1[start_state1] * len(map2) + map2[start_state2])

    for final_state1 in fa1.final_states:
        for final_state2 in fa2.final_states:
            ans.add_final_state(map1[final_state1] * len(map2) + map2[final_state2])

    return ans


def graph_regular_query(graph, start_states, final_states, regex) -> [Tuple]:
    """
    Query finite automaton built out of a graph with a regular expression.

    Args:
        graph: the graph for a NFA
        start_states: list of FA start states
        final_states: list of FA final states
        regex: regular expression string

    Returns:
        Set of pairs of achievable nodes numbers.
    """
    nfa = graph2nfa(graph, start_states, final_states)
    intersection = intersect_nfa(regex2dfa(regex), nfa)

    matrix, mapping = fa2matrix(intersection)
    rev_mapping = {i: v for v, i in mapping.items()}

    closure = sum(matrix.values())

    prev = closure.count_nonzero()
    cur = 0
    while prev != cur:
        closure += closure @ closure
        prev, cur = cur, closure.count_nonzero()

    ans = set()

    for source, dest in zip(*closure.nonzero()):
        if (
            rev_mapping[source] in intersection.start_states
            and rev_mapping[dest] in intersection.final_states
        ):
            ans.add(
                (
                    list(nfa.states)[rev_mapping[source].value % len(nfa.states)],
                    list(nfa.states)[rev_mapping[dest].value % len(nfa.states)],
                )
            )

    return ans
