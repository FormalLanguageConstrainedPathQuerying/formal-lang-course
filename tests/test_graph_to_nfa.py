import cfpq_data
from project.task2 import graph_to_nfa
import pytest
import networkx as nx


@pytest.mark.parametrize(
    "graph, start_states, final_states, expected_states, expected_start_states, expected_final_states",
    [
        # Testcase 1: basic graph with empty start and final states
        (cfpq_data.graph_from_csv(cfpq_data.download("bzip")), set(), set(), 632, 632, 632),

        # Testcase 2: basic graph with some empty start and final states
        (cfpq_data.graph_from_csv(cfpq_data.download("bzip")), {0, 1, 2}, {5, 6, 7, 8, 9}, 632, 3, 5),

        # Testcase 3: empty graph
        (nx.MultiDiGraph(), set(), set(), 0, 0, 0),

        # Testcase 4: non-existing start and final states
        (nx.MultiDiGraph(), {10000}, {20000}, 0, 0, 0)
    ]
)
def test_graph_to_nfa(graph, start_states, final_states, expected_states, expected_start_states, expected_final_states):
    nfa = graph_to_nfa(graph, start_states, final_states)

    assert len(nfa.states) == expected_states
    assert len(nfa.start_states) == expected_start_states
    assert len(nfa.final_states) == expected_final_states
