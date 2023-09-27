from pyformlang.regular_expression import Regex
from project.automaton_lib import nfa_of_graph
from project.automaton_lib import regular_path_query
from networkx.drawing.nx_pydot import read_dot
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton


def automaton_from_path(path: str) -> NondeterministicFiniteAutomaton:
    graph = read_dot(path)
    return nfa_of_graph(graph)


def test_regular_path_query():
    path = "tests/test_graphs/au1_graph.dot"
    regex = Regex("0 0 (1|0)*")
    graph = read_dot(path)

    result = regular_path_query(graph, ["0"], ["1"], regex)

    assert result == {("0", "1")}


def test_regular_path_query_harder():
    path = "tests/test_graphs/au2_graph.dot"
    regex = Regex("1* 0*")
    graph = read_dot(path)

    result = regular_path_query(graph, ["0", "3"], ["2", "3"], regex)

    assert result == {("3", "3")}
