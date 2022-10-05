import cfpq_data
from pyformlang.regular_expression import PythonRegex

from project.t2_finite_automata import (
    build_minimal_dfa_from_regex,
    build_nfa_from_graph,
)
from project.t3_boolean_matrix_automata import *


def test_rpq_with_separated():
    graph = cfpq_data.labeled_two_cycles_graph(3, 3, labels=("a", "b"))
    regex = PythonRegex("(a*|b)")
    bool_matrix_for_graph = BooleanMatrixAutomata(
        build_nfa_from_graph(graph, None, None)
    )
    bool_matrix_for_regex = BooleanMatrixAutomata(build_minimal_dfa_from_regex(regex))
    result = bool_matrix_for_graph.bfs_based_rpq(bool_matrix_for_regex, True)

    expected_result = {
        0: [0, 1, 2, 3, 4],
        1: [0, 1, 2, 3],
        2: [0, 1, 2, 3],
        3: [0, 1, 2, 3],
        4: [5],
        5: [6],
        6: [0],
    }

    assert result == expected_result


def test_rpq_without_separated():
    graph = cfpq_data.labeled_two_cycles_graph(3, 3, labels=("a", "b"))
    regex = PythonRegex("(a*|b)")
    bool_matrix_for_graph = BooleanMatrixAutomata(
        build_nfa_from_graph(graph, None, None)
    )
    bool_matrix_for_regex = BooleanMatrixAutomata(build_minimal_dfa_from_regex(regex))
    result = bool_matrix_for_graph.bfs_based_rpq(bool_matrix_for_regex, False)

    expected_result = {0, 1, 2, 3, 4, 5, 6}

    assert result == expected_result
