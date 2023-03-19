from project.fa_utils import regex2dfa, graph2nfa
from pyformlang.finite_automaton import EpsilonNFA
import networkx as nx
from networkx.classes.multidigraph import MultiDiGraph
import numpy as np
from scipy.sparse import dok_matrix, coo_matrix, kron, vstack, block_diag, identity

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


def get_reachable_vertices(
    regex_fa: EpsilonNFA,
    graph: MultiDiGraph,
    start_states: [int],
    for_each: bool = False,
):
    """
    Finds reachable vertices in a graph

    Args:
        regex_fa: regex finite automaton
        graph: graph to search
        start_states: list of states from which reachability will be searched
        for_each: a flag indicating whether the result will be displayed for each
                  start state separately, or together

    Returns:
        Set or dict of reachable states
    """
    (regex_matrices, regex_mapping) = fa2matrix(regex_fa)
    (graph_matrices, graph_mapping) = fa2matrix(graph)

    common_states = set(regex_matrices.keys()).intersection(set(graph_matrices.keys()))

    diag_transitions = {
        state: block_diag((regex_matrices[state], graph_matrices[state])).transpose()
        for state in common_states
    }

    if for_each:
        start_states_sets = {frozenset({x}) for x in start_states}
    else:
        start_states_sets = {frozenset(start_states)}

    result = {}
    for start_states in start_states_sets:
        cur = {
            (regex_mapping[r], graph_mapping[n])
            for r in regex_fa.start_states
            for n in start_states
        }

        used = set()
        while cur:
            used |= cur

            front = dok_matrix((len(graph_mapping), len(regex_mapping)), dtype=np.bool_)
            for (source, dest) in cur:
                front[dest, source] = True
            front = vstack(
                (identity(len(regex_mapping), dtype=np.bool_), front), format="csr"
            )

            cur = set()
            for label, matrix in diag_transitions.items():
                regex_states = [[]] * len(regex_mapping)
                graph_states = [[]] * len(regex_mapping)

                new_front = coo_matrix(matrix @ front)

                for source, dest, val in zip(
                    new_front.row, new_front.col, new_front.data
                ):
                    if val:
                        if source < len(regex_mapping):
                            regex_states[dest].append(source)
                        else:
                            graph_states[dest].append(source - len(regex_mapping))

                cur |= {
                    (source, dest)
                    for i in range(len(regex_mapping))
                    for source in regex_states[i]
                    for dest in graph_states[i]
                }

            cur -= used

        result[frozenset(start_states)] = {
            j for i, j in used if i in {regex_mapping[i] for i in regex_fa.final_states}
        }

    graph_states = [
        j for _, j in sorted([(id, label) for label, id in graph_mapping.items()])
    ]

    if for_each:
        return {
            state: {graph_states[dest] for dest in dests}
            for (state,), dests in result.items()
        }
    else:
        (ids,) = result.values()
        return {graph_states[id] for id in ids}


def bfs_graph_regular_query(
    graph: MultiDiGraph,
    start_states: [int],
    final_states: [int],
    regex: str,
    for_each: bool = False,
):
    """
    Queries graph regular expression

    Args:
        graph: a graph to query
        start_states: list of start states
        final_states: list of final states
        regex: regular expression string
        for_each: a flag indicating whether the result will be displayed for each
                  start state separately, or together

    Returns:
        Set or dict of states
    """
    regex_dfa = regex2dfa(regex)
    graph_nfa = graph2nfa(graph, [], [])

    result = get_reachable_vertices(regex_dfa, graph_nfa, start_states, for_each)

    if final_states is None or not for_each:
        return {state for state in result if state in final_states}

    if for_each:
        return {
            state: {dest for dest in dests if dest in final_states}
            for state, dests in result.items()
        }
