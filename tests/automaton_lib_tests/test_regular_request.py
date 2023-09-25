from pyformlang.regular_expression import Regex
from project.automaton_lib import nfa_of_graph
from project.automaton_lib import regular_request
from networkx.drawing.nx_pydot import read_dot
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton


def automaton_from_path(path: str) -> NondeterministicFiniteAutomaton:
    graph = read_dot(path)
    return nfa_of_graph(graph)


def test_regular_request():
    path = "tests/test_graphs/au1_graph.dot"
    regex = Regex("0 0 (1|0)*")
    graph = read_dot(path)

    regular_request(graph, ["0"], ["1"], regex)

    assert False
