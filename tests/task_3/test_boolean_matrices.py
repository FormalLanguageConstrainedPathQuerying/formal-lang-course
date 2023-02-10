import networkx as nx
import numpy as np
import pytest
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from tests.utils import read_data_from_json, dot_to_graph
from project.automata_tools import create_nfa_from_graph
from project.boolean_matrices import BooleanMatrices


@pytest.mark.parametrize(
    "input_bm, expected_bm, start_states, final_states",
    read_data_from_json(
        "test_bm_init",
        lambda data: (
            BooleanMatrices.from_automaton(
                create_nfa_from_graph(dot_to_graph(data["graph"]))
            ),
            data["expected_bm"],
            set(data["start_states"]),
            set(data["final_states"]),
        ),
    ),
)
def test_bm_init(input_bm: BooleanMatrices, expected_bm, start_states, final_states):
    is_correct = True
    for symbol, matrix in input_bm.bool_matrices.items():
        expected = expected_bm[symbol]
        is_correct = np.array_equal(matrix.toarray(), expected)
        if not is_correct:
            break
    assert (
        is_correct
        and input_bm.get_start_states() == start_states
        and input_bm.get_final_states() == final_states
    )


@pytest.mark.parametrize(
    "input_bm, expected_bm",
    read_data_from_json(
        "test_transitive_closure",
        lambda data: (
            BooleanMatrices.from_automaton(
                create_nfa_from_graph(dot_to_graph(data["graph"]))
            ),
            data["matrix"],
        ),
    ),
)
def test_transitive_closure(input_bm: BooleanMatrices, expected_bm):
    tc = input_bm.transitive_closure()
    assert np.array_equal(tc.toarray(), expected_bm)


@pytest.mark.parametrize(
    "input_bm, expected_automaton",
    read_data_from_json(
        "test_to_automaton",
        lambda data: (
            BooleanMatrices.from_automaton(
                create_nfa_from_graph(dot_to_graph(data["expected"]))
            ),
            create_nfa_from_graph(dot_to_graph(data["expected"])),
        ),
    ),
)
def test_to_automaton(input_bm: BooleanMatrices, expected_automaton):
    actual = input_bm.to_automaton()
    assert (
        nx.drawing.nx_pydot.to_pydot(actual.to_networkx()).__str__()
        == nx.drawing.nx_pydot.to_pydot(expected_automaton.to_networkx()).__str__()
    )


@pytest.mark.parametrize(
    "g1, g2, expected",
    read_data_from_json(
        "test_intersect",
        lambda data: (
            (
                create_nfa_from_graph(
                    dot_to_graph(data["graph1"]),
                    data["start_states1"],
                    data["final_states1"],
                )
            ),
            (
                create_nfa_from_graph(
                    dot_to_graph(data["graph2"]),
                    data["start_states2"],
                    data["final_states2"],
                )
            ),
            (
                create_nfa_from_graph(
                    dot_to_graph(data["graph_expected"]),
                    data["start_states_expected"],
                    data["final_states_expected"],
                )
            ),
        ),
    ),
)
def test_intersect(
    g1: NondeterministicFiniteAutomaton,
    g2: NondeterministicFiniteAutomaton,
    expected: NondeterministicFiniteAutomaton,
):
    bm1 = BooleanMatrices.from_automaton(g1)
    bm2 = BooleanMatrices.from_automaton(g2)
    intersection = bm1.intersect(bm2)

    actual = intersection.to_automaton()

    if len(expected.states) == 0:
        assert actual.to_networkx().__str__() == expected.to_networkx().__str__()
    else:
        assert actual.is_equivalent_to(expected)


@pytest.mark.parametrize(
    "self, other",
    read_data_from_json(
        "test_direct_sum",
        lambda data: (
            BooleanMatrices.from_automaton(
                create_nfa_from_graph(
                    dot_to_graph(data["g1"]), set(data["starts1"]), set(data["finals1"])
                )
            ),
            BooleanMatrices.from_automaton(
                create_nfa_from_graph(
                    dot_to_graph(data["g2"]), set(data["starts2"]), set(data["finals2"])
                )
            ),
        ),
    ),
)
def test_direct_sum(self: BooleanMatrices, other: BooleanMatrices):
    d_sum = self.direct_sum(other)
    pass
