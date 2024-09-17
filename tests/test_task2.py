import cfpq_data

from project.task1 import get_graph_data, save_labeled_two_cycles_graph
from project.task2 import regex_to_dfa, graph_to_nfa
from networkx import nx_pydot
import pytest


def test_regex_to_dfa():
    dfa = regex_to_dfa("a*b")
    assert dfa.accepts("aaab")
    assert dfa.accepts("b")
    assert not dfa.accepts("abb")


@pytest.mark.parametrize("name", ["wc", "ls"])
def test_graph_to_nfa(name):
    path = cfpq_data.download(name)
    graph = cfpq_data.graph_from_csv(path)

    graph_data = get_graph_data(name)
    nfa = graph_to_nfa(graph, set(), set())

    start_states = nfa.start_states
    final_states = nfa.final_states
    states = nfa.states

    assert start_states == final_states == states
    assert len(states) == graph_data.node_count
    assert nfa.symbols == set(graph_data.labels)


@pytest.mark.parametrize(
    "n, m, labels, dot_filename",
    [
        (3, 4, ["a", "b"], "graph_3_4_ab.dot"),
        (5, 5, ["x", "y"], "graph_5_5_xy.dot"),
        (2, 3, ["label1", "label2"], "graph_2_3_label1_label2.dot"),
    ],
)
def test_two_cycled_graph_to_nfa(tmp_path, n, m, labels, dot_filename):
    test_path = tmp_path / "test.dot"

    save_labeled_two_cycles_graph(n, m, labels, test_path)

    graph = nx_pydot.read_dot(str(test_path))
    nfa = graph_to_nfa(graph, set(), set())

    start_states = nfa.start_states
    final_states = nfa.final_states
    all_states = nfa.states

    assert start_states == final_states == all_states
    assert len(all_states) == n + m + 1
    assert nfa.symbols == set(labels)
