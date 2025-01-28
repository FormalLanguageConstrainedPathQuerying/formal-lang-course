import cfpq_data
import pytest
from networkx import MultiDiGraph
from pyformlang.finite_automaton import State

from project.hw2.graph_to_nfa_tool import (
    graph_to_nfa,
)
from project.hw1.graph_builder import load_graph


@pytest.mark.parametrize("graph_name", ["travel", "skos"])
def test_graph_to_nfa_from_file(graph_name: str):
    graph = cfpq_data.graph_from_csv(cfpq_data.download(graph_name))
    graph_data = load_graph(graph_name)
    nfa = graph_to_nfa(graph, set(), set())

    start_states = set(int(st.value) for st in nfa.start_states)
    final_states = set(int(st.value) for st in nfa.final_states)
    all_states = set(int(st.value) for st in nfa.states)

    assert start_states == final_states == all_states
    assert len(all_states) == graph_data.nodes_cnt
    assert nfa.symbols == graph_data.labels


def test_graph_to_nfa_synthetic():
    graph = MultiDiGraph()
    graph.add_nodes_from({0, 1, 2, 3, 4, 5})
    graph.add_edges_from(
        [
            (0, 1, {"label": "test1"}),
            (1, 2, {"label": "test2"}),
            (2, 1, {"label": "test1"}),
            (2, 3, {"label": "test3"}),
            (3, 5, {"label": "test4"}),
            (3, 4, {"label": "test"}),
            (4, 5, {"label": "tst"}),
        ]
    )
    nfa = graph_to_nfa(graph, {1}, {5})
    assert nfa.start_states == {State(1)}
    assert nfa.final_states == {State(5)}
    assert len(nfa.states) == len(graph.nodes)


def test_graph_to_nfa_synthetic_empty_start():
    graph = MultiDiGraph()
    graph.add_nodes_from({0, 1, 2, 3, 4, 5})
    graph.add_edges_from(
        [
            (0, 1, {"label": "test1"}),
            (1, 2, {"label": "test2"}),
            (2, 1, {"label": "test1"}),
            (2, 3, {"label": "test3"}),
            (3, 5, {"label": "test4"}),
            (3, 4, {"label": "test"}),
            (4, 5, {"label": "tst"}),
        ]
    )
    nfa = graph_to_nfa(graph, set(), {5})
    assert len(nfa.start_states) == len(graph.nodes)
    assert nfa.final_states == {State(5)}
    assert len(nfa.states) == len(graph.nodes)


def test_graph_to_nfa_synthetic_empty_final():
    graph = MultiDiGraph()
    graph.add_nodes_from({0, 1, 2, 3, 4, 5})
    graph.add_edges_from(
        [
            (0, 1, {"label": "test1"}),
            (1, 2, {"label": "test2"}),
            (2, 1, {"label": "test1"}),
            (2, 3, {"label": "test3"}),
            (3, 5, {"label": "test4"}),
            (3, 4, {"label": "test"}),
            (4, 5, {"label": "tst"}),
        ]
    )
    nfa = graph_to_nfa(graph, {1}, set())
    assert nfa.start_states == {State(1)}
    assert len(nfa.final_states) == len(graph.nodes)
    assert len(nfa.states) == len(graph.nodes)


def test_graph_to_nfa_synthetic_empty_start_final():
    graph = MultiDiGraph()
    graph.add_nodes_from({0, 1, 2, 3, 4, 5})
    graph.add_edges_from(
        [
            (0, 1, {"label": "test1"}),
            (1, 2, {"label": "test2"}),
            (2, 1, {"label": "test1"}),
            (2, 3, {"label": "test3"}),
            (3, 5, {"label": "test4"}),
            (3, 4, {"label": "test"}),
            (4, 5, {"label": "tst"}),
        ]
    )
    nfa = graph_to_nfa(graph, set(), set())
    assert len(nfa.start_states) == len(graph.nodes)
    assert len(nfa.final_states) == len(graph.nodes)
    assert len(nfa.states) == len(graph.nodes)
