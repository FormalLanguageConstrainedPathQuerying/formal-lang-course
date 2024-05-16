import pytest

try:
    from project.task2.dfa_builder import regex_to_dfa
    from project.task2.nfa_builder import graph_to_nfa
except ImportError:
    pytestmark = pytest.mark.skip("Task 2 is not ready to test!")
from networkx import MultiDiGraph


class TestExceptionCases:
    def test_invalid_regex(self):
        with pytest.raises(ValueError, match="Invalid regular expression"):
            regex_to_dfa(")(")

    def test_invalid_nodes(self):
        graph = MultiDiGraph()
        graph.add_edge(1, 2, label="a")
        start_states = {1}
        final_states = {2, 3}  # 3 is not in the graph
        with pytest.raises(ValueError, match="Nodes are not subset of graph"):
            graph_to_nfa(graph, start_states, final_states)
