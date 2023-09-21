from networkx import MultiDiGraph
from networkx.drawing.nx_pydot import read_dot
from project.automaton_lib import nfa_of_graph


def test_nfa_of_empty_graph():
    nfa = nfa_of_graph(MultiDiGraph())

    assert nfa.is_empty()


def test_nfa_of_graph_rewrite_start_and_final():
    path = "tests/test_graphs/nfa_graph.dot"
    graph = read_dot(path)
    nfa = nfa_of_graph(graph, starting_nodes=["0"], final_nodes=["0"])

    assert nfa.accepts("")
    assert nfa.accepts("abc")
    assert nfa.accepts("abcabc")

    assert not nfa.accepts("abcab")
    assert not nfa.accepts("abcab")
    assert not nfa.accepts("d")
    assert not nfa.accepts("bca")
    assert not nfa.accepts("c")


def test_nfa_of_graph_rewrite_start():
    path = "tests/test_graphs/nfa_graph.dot"
    graph = read_dot(path)
    nfa = nfa_of_graph(graph, starting_nodes=["0"])

    assert nfa.accepts("")
    assert nfa.accepts("abc")
    assert nfa.accepts("abcabc")
    assert nfa.accepts("abcab")
    assert nfa.accepts("abcab")

    assert not nfa.accepts("d")
    assert not nfa.accepts("bca")
    assert not nfa.accepts("aba")
    assert not nfa.accepts("c")


def test_nfa_of_graph():
    path = "tests/test_graphs/nfa_graph.dot"
    graph = read_dot(path)
    nfa = nfa_of_graph(graph)

    assert nfa.accepts("")
    assert nfa.accepts("bcabc")
    assert nfa.accepts("abc")
    assert nfa.accepts("bc")
    assert nfa.accepts("c")

    assert not nfa.accepts("bab")
    assert not nfa.accepts("bcac")
    assert not nfa.accepts("aba")
    assert not nfa.accepts("cd")
