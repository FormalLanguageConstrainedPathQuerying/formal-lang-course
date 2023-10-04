from pyformlang.regular_expression import Regex
from project.automaton_lib import binary_matrices_of_automaton
from project.automaton_lib import nfa_of_graph
from networkx.drawing.nx_pydot import read_dot


def test_binary_matrices_of_automaton():
    path = "tests/test_graphs/tc_graph.dot"
    graph = read_dot(path)
    automaton = nfa_of_graph(graph)

    result = binary_matrices_of_automaton(automaton)

    assert len(result) == 1
    assert result[0].starting_nodes == {"0", "1", "2", "3"}
    assert result[0].final_nodes == {"0", "1", "2", "3"}
    assert len(result[0].matrix.nonzero()[0]) == 2
    assert result[0].label == "a"
