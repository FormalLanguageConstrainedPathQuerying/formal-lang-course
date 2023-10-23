from project.automaton_lib import get_reachable_nodes_constrained
from project.automaton_lib import get_reachable_final_nodes_constrained
from networkx.drawing.nx_pydot import read_dot
from pyformlang.regular_expression import Regex


def test_constrained_bfs_1():
    graph = read_dot("tests/test_graphs/nfa_graph.dot")
    regex = Regex("")
    result = get_reachable_nodes_constrained(graph, regex, ["2", "1"], True)

    assert result == {"1": "1", "2": "2"}


def test_constrained_bfs_2():
    graph = read_dot("tests/test_graphs/nfa_graph.dot")
    regex = Regex("a|b|c")
    result = get_reachable_nodes_constrained(graph, regex, ["1"], False)

    assert result == {"2"}


def test_constrained_bfs_3():
    graph = read_dot("tests/test_graphs/nfa_graph.dot")
    regex = Regex("(a|b|c)*")
    result = get_reachable_nodes_constrained(graph, regex, ["0"], False)

    assert result == {"1", "2", "0"}


def test_constrained_bfs_4():
    graph = read_dot("tests/test_graphs/nfa_graph.dot")
    regex = Regex("(a|b|c)*")
    result = get_reachable_nodes_constrained(graph, regex, ["2", "1"], True)

    assert result == {"1": {"1", "2", "0"}, "2": {"1", "2", "0"}}


def test_constrained_bfs_5():
    graph = read_dot("tests/test_graphs/nfa_graph.dot")
    regex = Regex("(a|b|c)*")
    result = get_reachable_final_nodes_constrained(
        graph, regex, ["2", "1"], {"1", "0"}, False
    )

    assert result == {"1", "0"}


def test_constrained_bfs_6():
    graph = read_dot("tests/test_graphs/nfa_graph.dot")
    regex = Regex("(a|b|c)*")
    result = get_reachable_final_nodes_constrained(
        graph, regex, ["2", "1"], {"1", "0"}, True
    )

    assert result == {"1": {"1", "0"}, "2": {"1", "0"}}
