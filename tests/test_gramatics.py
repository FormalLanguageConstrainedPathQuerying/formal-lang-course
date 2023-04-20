import cfpq_data as cfpq
import pytest
from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Variable, Production, Terminal

from project.gramatics import *


def assert_cfgs(a: CFG, b: CFG):
    assert a.start_symbol == b.start_symbol
    assert a.productions == b.productions


def test_cfg_to_wcnf():
    i = CFG.from_text("S -> a b")
    a = convert_to_weak_form(i)
    e = CFG.from_text(
        'S -> "VAR:a#CNF#" "VAR:b#CNF#" \n "VAR:a#CNF#" -> a \n "VAR:b#CNF#" -> b'
    )

    assert_cfgs(a, e)


def test_cfg_to_wcnf_complex():
    i = CFG.from_text("S -> A S B | c\nB -> b\nA -> a")
    a = convert_to_weak_form(i)
    e = CFG.from_text('S -> A "VAR:C#CNF#1" | c\nC#CNF#1 -> S B\nB -> b\nA -> a')

    assert_cfgs(a, e)


def get_graph_with_cfg():
    ge = [
        (0, 1, {"label": "a"}),
        (2, 0, {"label": "a"}),
        (1, 2, {"label": "a"}),
        (2, 3, {"label": "b"}),
        (3, 2, {"label": "b"}),
    ]
    g = MultiDiGraph()
    g.add_edges_from(ge)

    c = """
            S -> A B
            S -> A C
            A -> a
            B -> b
            C -> S B
           """

    return g, c


def test_helings_algorithm():
    g, c = get_graph_with_cfg()

    e = {(Variable("A"), 0, 1), (Variable("A"), 1, 2), (Variable("A"), 2, 0), (Variable("B"), 2, 3), (Variable("B"), 3, 2)}
    e = e.union([(Variable("C"), i, j) for j in range(2, 4) for i in range(0, 3)])
    e = e.union([(Variable("S"), i, j) for j in range(2, 4) for i in range(0, 3)])

    hr = hellings_algorithm(g, c)
    assert len(hr.difference(e)) == 0


def test_query_cfg_graph():
    graph, cfg = get_graph_with_cfg()
    ss = {0, 1}
    fs = {2}
    qr = query_graph_with_cfg(graph, cfg, ss, fs)
    assert qr == {(0, 2), (1, 2)}