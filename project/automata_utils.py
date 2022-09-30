import numpy as np
from pyformlang.pda import Symbol
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import DeterministicFiniteAutomaton, EpsilonNFA, State
from scipy.sparse import coo_matrix, kron, find

__all__ = [
    "from_regex_to_dfa",
    "intersect_enfa",
    "boolean_decompose_enfa",
]

from project.boolean_decomposition import BooleanDecomposition, boolean_decompose_enfa


def from_regex_to_dfa(regex: Regex) -> DeterministicFiniteAutomaton:
    """
    Converts regex to DFA

    :param regex: regex to be converted
    :return: DeterministicFiniteAutomaton object representing given regex
    """
    return regex.to_epsilon_nfa().to_deterministic().minimize()


def intersect_enfa(enfa1: EpsilonNFA, enfa2: EpsilonNFA) -> EpsilonNFA:
    """
    Find intersection of 2 EpsilonNFA
    :return: EpsilonNFA representing intersection of enfa1 and enfa2
    """
    decomposition1 = boolean_decompose_enfa(enfa1)
    decomposition2 = boolean_decompose_enfa(enfa2)

    intersection_decomposition = decomposition1.kron(decomposition2)

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
