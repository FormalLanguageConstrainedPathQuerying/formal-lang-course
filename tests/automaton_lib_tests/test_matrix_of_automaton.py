from pyformlang.regular_expression import Regex
from project.automaton_lib import binary_matrices_of_automaton
from project.automaton_lib import nfa_of_graph
from networkx.drawing.nx_pydot import read_dot


def test_binary_matrices_of_automaton():
    path = "tests/test_graphs/tc_graph.dot"
    graph = read_dot(path)
    automaton = nfa_of_graph(graph)
    result = binary_matrices_of_automaton(automaton)

    assert False
