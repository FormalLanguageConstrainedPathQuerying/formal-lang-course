from project.grammar_lib import (
    ecfg_of_file,
    ecfg_of_cfg,
    cfg_of_path,
    hellings_path_query,
)
from project.extended_context_free_grammar import ECFG
from pyformlang.cfg import Variable, Terminal
from pyformlang.regular_expression import Regex
from networkx.drawing.nx_pydot import read_dot


def test_hellings_pq_1():
    graph_path = "tests/test_graphs/nfa_graph.dot"
    cfg_path = "tests/test_grammars/hellings_1.cfg"
    graph = read_dot(graph_path)
    cfg = cfg_of_path(cfg_path)
    reachable = hellings_path_query(graph, cfg)

    assert {("0", "0"), ("1", "1"), ("2", "2"), ("0", "1"), ("1", "2")} == reachable


def test_hellings_pq_2():
    graph_path = "tests/test_graphs/nfa_graph.dot"
    cfg_path = "tests/test_grammars/hellings_2.cfg"
    graph = read_dot(graph_path)
    cfg = cfg_of_path(cfg_path)
    reachable = hellings_path_query(graph, cfg)

    assert {("0", "1"), ("1", "2")} == reachable


def test_hellings_pq_3():
    graph_path = "tests/test_graphs/au2_graph.dot"
    cfg_path = "tests/test_grammars/hellings_3.cfg"
    graph = read_dot(graph_path)
    cfg = cfg_of_path(cfg_path)
    reachable = hellings_path_query(graph, cfg)

    assert {("1", "2"), ("0", "0"), ("2", "2"), ("3", "3")} == reachable


def test_hellings_pq_4():
    graph_path = "tests/test_graphs/au2_graph.dot"
    cfg_path = "tests/test_grammars/hellings_4.cfg"
    graph = read_dot(graph_path)
    cfg = cfg_of_path(cfg_path)
    reachable = hellings_path_query(graph, cfg)

    assert {
        ("3", "3"),
        ("1", "2"),
        ("2", "2"),
        ("0", "1"),
        ("1", "1"),
        ("0", "0"),
    } == reachable
