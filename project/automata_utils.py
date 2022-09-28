import numpy as np
from pyformlang.pda import Symbol
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton, EpsilonNFA, State
from scipy.sparse import coo_matrix, kron, find

__all__ = [
    "from_regex_to_dfa",
    "intersect_enfa",
    "boolean_decompose_enfa",
    "kron_boolean_decompositions",
]

from project.boolean_decomposition import BooleanDecomposition


def from_regex_to_dfa(regex: Regex) -> DeterministicFiniteAutomaton:
    """
    Converts regex to DFA

    :param regex: regex to be converted
    :return: DeterministicFiniteAutomaton object representing given regex
    """
    return regex.to_epsilon_nfa().to_deterministic().minimize()


def boolean_decompose_enfa(enfa: EpsilonNFA) -> BooleanDecomposition:
    """
    Produce boolean decomposition of EpsilonNFA

    :param enfa: EpsilonNFA to be decomposed
    :return: boolean decomposition of EpsilonNFA
    """
    states_data = list(enfa.states)
    boolean_decompose = dict()
    for (u, symbol_and_vs) in enfa.to_dict().items():
        for (symbol, vs) in symbol_and_vs.items():
            if symbol not in boolean_decompose:
                boolean_decompose[symbol] = list()
            if not type(vs) is set:  # vs is one state in this case
                boolean_decompose[symbol].append(
                    (states_data.index(u), states_data.index(vs))
                )
            else:
                for v in vs:
                    boolean_decompose[symbol].append(
                        (states_data.index(u), states_data.index(v))
                    )

    states_num = len(enfa.states)
    coo_matrices = dict()
    for (symbol, edges) in boolean_decompose.items():
        row = np.array([i for (i, _) in edges])
        col = np.array([j for (_, j) in edges])
        data = np.array([1 for _ in range(len(edges))])
        coo_matrices[symbol] = coo_matrix(
            (data, (row, col)), shape=(states_num, states_num)
        )

    return BooleanDecomposition(coo_matrices, states_data)


def kron_boolean_decompositions(
    decomposition1: BooleanDecomposition, decomposition2: BooleanDecomposition
) -> BooleanDecomposition:
    """
    Produces kronecker production between matrices with same symbols in boolean decompositions
    :return: boolean decomposition of intersection of finite automatas, represented by decomposition1 and
    decomposition2. States in this decomposition as values have 2 element tuples (state1, state2), where state1 from
    decomposition1, and state2 from decomposition2
    """
    intersection_decomposition = dict()
    dict1 = decomposition1.to_dict()
    dict2 = decomposition2.to_dict()
    symbols = set(dict1.keys()).union(set(dict2.keys()))
    for symbol in symbols:
        if symbol in dict1:
            coo_matrix1 = dict1[symbol]
        else:
            coo_matrix1 = coo_matrix(
                (decomposition1.states_count(), decomposition1.states_count())
            )

        if symbol in dict2:
            coo_matrix2 = dict2[symbol]
        else:
            coo_matrix2 = coo_matrix(
                (decomposition2.states_count(), decomposition2.states_count())
            )

        intersection_decomposition[symbol] = kron(coo_matrix1, coo_matrix2)

    intersection_states = list()
    for state1 in decomposition1.states():
        for state2 in decomposition2.states():
            intersection_states.append(State((state1, state2)))

    return BooleanDecomposition(intersection_decomposition, intersection_states)


def intersect_enfa(enfa1: EpsilonNFA, enfa2: EpsilonNFA) -> EpsilonNFA:
    """
    Find intersection of 2 EpsilonNFA
    :return: EpsilonNFA representing intersection of enfa1 and enfa2
    """
    decomposition1 = boolean_decompose_enfa(enfa1)
    decomposition2 = boolean_decompose_enfa(enfa2)

    intersection_decomposition = kron_boolean_decompositions(
        decomposition1, decomposition2
    )

    start_states = list()
    for state1 in enfa1.start_states:
        for state2 in enfa2.start_states:
            start_states.append(State((state1, state2)))

    final_states = list()
    for state1 in enfa1.final_states:
        for state2 in enfa2.final_states:
            final_states.append(State((state1, state2)))

    intersection_nfa = EpsilonNFA()
    intersection_states = intersection_decomposition.states()
    for (symbol, matrix) in intersection_decomposition.to_dict().items():
        (rows, cols, _) = find(matrix)
        assert len(cols) == len(rows)
        for i in range(len(cols)):
            intersection_nfa.add_transition(
                intersection_states[rows[i]], symbol, intersection_states[cols[i]]
            )

    for start_state in start_states:
        intersection_nfa.add_start_state(start_state)

    for final_state in final_states:
        intersection_nfa.add_final_state(final_state)

    return intersection_nfa
