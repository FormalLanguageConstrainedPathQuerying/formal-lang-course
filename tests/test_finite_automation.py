from networkx import MultiDiGraph
from pyformlang.finite_automaton import State
from pyformlang.finite_automaton.nondeterministic_finite_automaton import (
    NondeterministicFiniteAutomaton,
)
from project.finite_automaton import graph_to_nfa
from project.graph_tools import GraphData
import pytest
import cfpq_data


@pytest.fixture
def graph(graph_name: str) -> MultiDiGraph:
    return cfpq_data.graph_from_csv(cfpq_data.download(graph_name))


@pytest.fixture
def nfa(
    graph: MultiDiGraph,
    start_states: set[int],
    final_states: set[int],
):
    return graph_to_nfa(graph, start_states=start_states, final_states=final_states)


def get_states_int(states: set[State]) -> set[int]:
    return set(int(s.value) for s in states)


@pytest.mark.parametrize("graph_name", ["wc", "enzyme"])
@pytest.mark.parametrize("start_states", [{0, 1, 2}, {}])
@pytest.mark.parametrize("final_states", [{2}, {}])
def test_graph_to_nfa(
    graph: MultiDiGraph,
    graph_name: str,
    nfa: NondeterministicFiniteAutomaton,
    start_states: set[int],
    final_states: set[int],
):
    all_states = nfa.states
    start_states = start_states or all_states
    final_states = final_states or all_states

    assert start_states == get_states_int(nfa.start_states), "Start states don't match"
    assert final_states == get_states_int(nfa.final_states), "Final states don't match"
    assert set(map(int, graph.nodes)) == get_states_int(
        nfa.states
    ), "All states don't match"

    assert (
        GraphData.get_graph_data_by_name(graph_name).labels == nfa.symbols
    ), "Labels don't match symbols"
