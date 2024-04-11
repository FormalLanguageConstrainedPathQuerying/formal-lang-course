import pytest
from project.task6 import *
from pyformlang.cfg import CFG, Variable
from pyformlang.cfg import Production, Variable, Terminal, CFG, Epsilon
import networkx as nx
from pyformlang.cfg import CFG
import os


def test_grammar_weak1():

    g = read_cfgrammar("tests/filesForTest/cfgTest1")

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

    actual = cfg_to_weak_normal_form(read_cfgrammar("tests/filesForTest/cfgTest2"))
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
