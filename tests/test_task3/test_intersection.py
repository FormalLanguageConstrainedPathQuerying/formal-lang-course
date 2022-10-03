import networkx as nx
import pytest
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton

from project.boolean_decompositon import (
    get_intersect_boolean_decomposition,
    decomposition_to_automaton,
)
from project.regex_utils import create_nfa_from_graph
from project.rpq import (
    BooleanDecomposition,
)
from tests.test_task3.utils import get_data, dot_to_graph


@pytest.mark.parametrize(
    "graph1, graph2, expected",
    get_data(
        "test_intersection",
        lambda data: (
            create_nfa_from_graph(
                dot_to_graph(data["graph1"]),
                start_states=set(data["starts1"]),
                final_states=set(data["finals1"]),
            ),
            create_nfa_from_graph(
                dot_to_graph(data["graph2"]),
                set(data["starts2"]),
                final_states=set(data["finals2"]),
            ),
            create_nfa_from_graph(
                dot_to_graph(data["expected"]),
                set(data["starts_expected"]),
                final_states=set(data["finals_expected"]),
            ),
        ),
    ),
)
def test_intersection(
    graph1: NondeterministicFiniteAutomaton,
    graph2: NondeterministicFiniteAutomaton,
    expected: NondeterministicFiniteAutomaton,
):
    decomposition1 = BooleanDecomposition(graph1)
    decomposition2 = BooleanDecomposition(graph2)

    intersected = get_intersect_boolean_decomposition(decomposition1, decomposition2)

    actual = decomposition_to_automaton(intersected)

    if len(expected.states) == 0:
        assert actual.to_networkx().__str__() == expected.to_networkx().__str__()
    else:
        assert actual.is_equivalent_to(expected)
