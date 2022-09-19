import pytest
from pyformlang.regular_expression import PythonRegex

from project.__init__ import *


def test_equivalence_min_dfa_by_regex(expected_dfa):
    regex = PythonRegex("ac*|ded")
    dfa = create_min_dfa_by_regex(regex)

    assert dfa.is_equivalent_to(expected_dfa)
    assert dfa.accepts("acccc")
    assert dfa.accepts("a")
    assert dfa.accepts("ded")


@pytest.mark.parametrize(
    "two_cycles_graph", [[3, 3, "a", "b"]], indirect=["two_cycles_graph"]
)
def test_create_nfa_by_graph_with_st_fin_states(two_cycles_graph):
    nfa = create_nfa_by_graph(two_cycles_graph, [0, 1], [5, 6])

    assert nfa.get_number_transitions() == 8
    assert nfa.start_states == {0, 1}
    assert nfa.final_states == {5, 6}


@pytest.mark.parametrize(
    "two_cycles_graph", [[3, 3, "a", "b"]], indirect=["two_cycles_graph"]
)
def test_create_nfa_by_graph_without_st_fin_states(two_cycles_graph):
    nfa = create_nfa_by_graph(two_cycles_graph)

    assert nfa.get_number_transitions() == 8
    assert nfa.start_states == {0, 1, 2, 3, 4, 5, 6}
    assert nfa.final_states == {0, 1, 2, 3, 4, 5, 6}


@pytest.mark.parametrize(
    "two_cycles_graph", [[1, 3, "a", "b"]], indirect=["two_cycles_graph"]
)
def test_equivalence_nfa_by_graph(two_cycles_graph, expected_nfa):
    nfa = create_nfa_by_graph(two_cycles_graph, [0], [4])

    assert nfa.is_equivalent_to(expected_nfa)
