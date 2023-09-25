from pyformlang.regular_expression import Regex
from project.automaton_lib import intersect_automatons
from project.automaton_lib import nfa_of_graph
from networkx.drawing.nx_pydot import read_dot
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton


def automaton_from_path(path: str) -> NondeterministicFiniteAutomaton:
    graph = read_dot(path)
    return nfa_of_graph(graph)


def test_automaton_intersection():
    first_path = "tests/test_graphs/au1_graph.dot"
    second_path = "tests/test_graphs/au2_graph.dot"
    first_automaton = automaton_from_path(first_path)
    second_automaton = automaton_from_path(second_path)

    result = intersect_automatons(first_automaton, second_automaton)

    assert False
