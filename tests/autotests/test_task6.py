import pytest
from project.task6 import *
from pyformlang.cfg import CFG, Variable
from pyformlang.cfg import Production, Variable, Terminal, CFG, Epsilon
import networkx as nx
from pyformlang.cfg import CFG


def test_grammar_weak1():

    g = read_cfgrammar("filesForTest/cfgTest1")

    actual = cfg_to_weak_normal_form(g)

    expected = CFG(
        {Variable("S")},
        {Terminal("a"), Terminal("b")},
        Variable("S"),
        {
            Production(Variable("S"), [Epsilon()]),
            Production(Variable("S"), [Variable("a#CNF#"), Variable("C#CNF#1")]),
            Production(Variable("C#CNF#1"), [Variable("S"), Variable("b#CNF#")]),
            Production(Variable("a#CNF#"), [Variable("a")]),
            Production(Variable("b#CNF#"), [Variable("b")]),
        },
    )

    assert actual.productions == expected.productions


def test_grammar_weak2():

    actual = cfg_to_weak_normal_form(read_cfgrammar("filesForTest/cfgTest2"))
    expected = CFG.from_text(
        """
    S -> NP VP
    VP -> V NP
    V -> foo
    V -> quu
    NP -> boo
    NP -> shoo
    """
    )

    assert actual.productions == expected.productions


def test_cfpq_with_hellings_happy_path():
    cfg = CFG.from_text("S -> a S b | ε")
    graph = nx.DiGraph()
    graph.add_edge(0, 1, label="a")
    graph.add_edge(1, 2, label="b")
    expected = {(0, 0), (1, 1), (2, 2), (0, 2)}
    actual = cfpq_with_hellings(cfg, graph)
    assert actual == expected


def test_cfpq_with_hellings_no_path():
    cfg = CFG.from_text("S -> a S b | ε")
    graph = nx.DiGraph()
    graph.add_edge(0, 1, label="a")
    graph.add_edge(2, 3, label="b")
    expected = {(0, 0), (1, 1), (2, 2), (3, 3)}
    actual = cfpq_with_hellings(cfg, graph)
    assert actual == expected


def test_cfpq_with_hellings_empty_graph():
    cfg = CFG.from_text("S -> a S b | ε")
    graph = nx.DiGraph()
    expected = set()
    actual = cfpq_with_hellings(cfg, graph)
    assert actual == expected


def test():
    cfg = CFG.from_text(
        """
    S -> ε
    S -> A N1
    N1 -> S B
    A -> a
    B -> b
    """
    )
    graph = nx.DiGraph()
    graph.add_edge(0, 1, label="a")
    graph.add_edge(1, 0, label="a")
    graph.add_edge(1, 2, label="b")
    graph.add_edge(2, 3, label="b")
    graph.add_edge(3, 1, label="b")
    actual = cfpq_with_hellings(cfg, graph)
    assert (0, 1) in actual
